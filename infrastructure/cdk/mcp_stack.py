from __future__ import annotations

import aws_cdk as cdk
from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
)
from constructs import Construct


class McpCdkStack(Stack):
    """
    Provisions a single EC2 instance that:
      - lives in the default VPC (public subnet with a public IP)
      - allows SSH (22) and app port (8000) only from your IP/CIDR
      - clones your repo into /opt/mcp
      - creates a venv /opt/mcp/venv
      - installs fastmcp, uvicorn[standard], python-dotenv
      - runs Uvicorn via systemd: /opt/mcp/venv/bin/uvicorn server.server:app --app-dir /opt/mcp ...
    Context keys you can pass at deploy time:
      - repoUrl          (str, required) e.g. https://github.com/d-abhishek/mcp-prompt-library.git
      - repoBranch       (str, optional) e.g. main (default: main)
      - allowedIpCidr    (str, required) e.g. 203.0.113.45/32 (your public IP)
      - instanceType     (str, optional) e.g. t3.small (default: t3.small)
      - keyPairName      (str, optional) existing EC2 key pair to allow SSH
    """

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)


        vpc = ec2.Vpc.from_lookup(self, "VPC", is_default=True)

        sg = ec2.SecurityGroup(self, "McpSg",
            vpc=vpc,
            allow_all_outbound=True,
            description="Security group for MCP EC2 instance",
        )
        sg.add_ingress_rule(
            ec2.Peer.ipv4("141.70.80.34/32"),
            ec2.Port.tcp(22),
            "SSH from my IP",
        )
        sg.add_ingress_rule(
            ec2.Peer.ipv4("141.70.80.34/32"),
            ec2.Port.tcp(8000),
            "Uvicorn / MCP from my IP",
        )
        sg.add_ingress_rule(
            ec2.Peer.ipv4("0.0.0.0/0"),
            ec2.Port.tcp(80),
            "HTTP from anywhere",
        )
        sg.add_ingress_rule(
            ec2.Peer.ipv4("0.0.0.0/0"),
            ec2.Port.tcp(443),
            "HTTPS from anywhere",
        )

        repo_url = "https://github.com/d-abhishek/mcp-prompt-library.git"
        repo_branch = "ec2-deployment"
        duckdns_token = "0c92a7f8-e769-455c-a157-4eaf2ba646f4"
        domain_name = "xl2-mcp.duckdns.org"

        user_data = ec2.UserData.for_linux()
        user_data.add_commands(
            # ===== System prep =====
            "set -euxo pipefail",
            "sudo dnf -y update",
            "sudo dnf -y install python3.13 python3.13-pip git cronie socat nginx",
            "sudo systemctl enable --now crond nginx",

            # ===== App dir + venv =====
            "sudo install -o ec2-user -g ec2-user -d /opt/mcp",
            "cd /opt/mcp",
            "python3.13 -m venv venv",
            "source venv/bin/activate",
            "python -m pip install --upgrade pip",

            # ===== Clone repo (idempotent) =====
            f'if [ ! -d ".git" ]; then git clone --branch "{repo_branch}" "{repo_url}" repo; fi',
            "mv repo/* repo/.* . 2>/dev/null || true",
            "rmdir repo",

            # ===== Install runtime deps =====
            "python -m pip install -e .",

            # ===== systemd unit for FastMCP =====
            "sudo tee /etc/systemd/system/fastmcp.service > /dev/null <<'UNIT'",
            "[Unit]",
            "Description=FastMCP (Uvicorn) - mcp-prompt-library",
            "After=network.target",
            "",
            "[Service]",
            "User=ec2-user",
            "WorkingDirectory=/opt/mcp",
            'Environment="PATH=/opt/mcp/venv/bin"',
            "ExecStart=/opt/mcp/venv/bin/uvicorn server.server:app --host 0.0.0.0 --port 8000 --workers 1 --proxy-headers --timeout-keep-alive 75",
            "Restart=on-failure",
            "RestartSec=5",
            "",
            "[Install]",
            "WantedBy=multi-user.target",
            "UNIT",
            "sudo systemctl daemon-reload",
            "sudo systemctl enable fastmcp",
            "sudo systemctl restart fastmcp",

            # ===== ACME (DNS-01 via DuckDNS) — run as ec2-user, no .bashrc =====
            # Install acme.sh for ec2-user and issue cert for your domain
            f"sudo -u ec2-user -i bash -lc 'set -euo pipefail; "
            "curl -fsSL https://get.acme.sh | sh -s email=hhn.thesis@gmail.com; "
            "set +u; . ~/.acme.sh/acme.sh.env; set -u; "
            "~/.acme.sh/acme.sh --set-default-ca --server letsencrypt; "
            f"echo \"export DuckDNS_Token=\\\"{duckdns_token}\\\"\" >> ~/.acme.sh/account.conf; "
            f"~/.acme.sh/acme.sh --issue --dns dns_duckdns -d \"{domain_name}\" --dnssleep 300 --debug 2"
            "'",

            # Prepare nginx cert target (owned by ec2-user so renewals can write)
            f"sudo mkdir -p /etc/nginx/ssl/{domain_name}",
            f"sudo chown -R ec2-user:ec2-user /etc/nginx/ssl/{domain_name}",
            f"sudo chmod 700 /etc/nginx/ssl/{domain_name}",

            # Install certs to nginx paths and set reload hook
            f"sudo -u ec2-user -i bash -lc 'set -euo pipefail; "
            "set +u; . ~/.acme.sh/acme.sh.env; set -u; "
            f"~/.acme.sh/acme.sh --install-cert -d \"{domain_name}\" "
            f" --key-file /etc/nginx/ssl/{domain_name}/privkey.pem "
            f" --fullchain-file /etc/nginx/ssl/{domain_name}/fullchain.pem "
            " --reloadcmd \"sudo nginx -t && sudo systemctl reload nginx\""
            "'",

            # ===== Nginx reverse proxy (HTTPS → MCP on 127.0.0.1:8000) =====
            "sudo tee /etc/nginx/conf.d/mcp.conf >/dev/null <<'EOF'",
            "server {",
            "  listen 80;",
            f"  server_name {domain_name};",
            "  return 301 https://$host$request_uri;",
            "}",
            "",
            "server {",
            "  listen 443 ssl http2;",
            f"  server_name {domain_name};",
            "",
            f"  ssl_certificate     /etc/nginx/ssl/{domain_name}/fullchain.pem;",
            f"  ssl_certificate_key /etc/nginx/ssl/{domain_name}/privkey.pem;",
            "",
            "  # (optional) basic TLS hardening",
            "  ssl_protocols TLSv1.2 TLSv1.3;",
            "  ssl_ciphers HIGH:!aNULL:!MD5;",
            "",
            "  location / {",
            "    proxy_pass http://127.0.0.1:8000;",
            "    proxy_set_header Host $host;",
            "    proxy_set_header X-Real-IP $remote_addr;",
            "    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;",
            "    proxy_set_header X-Forwarded-Proto $scheme;",
            "  }",
            "}",
            "EOF",

            # ===== Validate config & reload nginx =====
            "sudo nginx -t",
            "sudo systemctl reload nginx",
            "sudo systemctl status nginx --no-pager",
        )

        instance = ec2.Instance(self, "McpInstance",
            vpc=vpc,
            instance_type=ec2.InstanceType("t3.small"),
            machine_image=ec2.MachineImage.latest_amazon_linux2023(),
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
            key_name="mcpPL",
            security_group=sg,
            user_data=user_data,
        )

        # ---- Outputs ----
        cdk.CfnOutput(self, "InstanceId", value=instance.instance_id)
        cdk.CfnOutput(self, "PublicDns", value=instance.instance_public_dns_name)
        cdk.CfnOutput(self, "PublicIp", value=instance.instance_public_ip)
        cdk.CfnOutput(
            self,
            "TestHealthCurl",
            value=f'curl -i http://{instance.instance_public_dns_name}:8000/health',
        )
        cdk.CfnOutput(
            self,
            "TestMcpCurl",
            value=f'curl -i http://{instance.instance_public_dns_name}:8000/mcp',
        )