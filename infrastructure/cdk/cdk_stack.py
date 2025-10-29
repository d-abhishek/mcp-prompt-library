from __future__ import annotations

import aws_cdk as cdk
from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
)
from constructs import Construct


class CdkStack(Stack):
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

        repo_url = "https://github.com/d-abhishek/mcp-prompt-library.git"
        repo_branch = "ec2-deployment"

        user_data = ec2.UserData.for_linux()
        user_data.add_commands(
            # System prep
            "set -euxo pipefail",
            "sudo dnf -y update",
            "sudo dnf -y install python3.13 python3.13-pip git",
            # App dir + venv
            "sudo install -o ec2-user -g ec2-user -d /opt/mcp",
            "cd /opt/mcp",
            "python3.13 -m venv venv",
            "source venv/bin/activate",
            "python -m pip install --upgrade pip",
            # Clone repo (idempotent: only if not already cloned)
            f'if [ ! -d ".git" ]; then git clone --branch "{repo_branch}" "{repo_url}" repo; fi',
            "mv repo/* repo/.* . 2>/dev/null || true",
            "rmdir repo",
            # Install runtime deps (simple & fast; you can switch to `pip install -e .` if desired)
            "python -m pip install -e .",
            # systemd unit
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
            "systemctl daemon-reload",
            "systemctl enable fastmcp",
            "systemctl restart fastmcp",
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
