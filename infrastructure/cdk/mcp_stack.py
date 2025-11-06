from __future__ import annotations

import aws_cdk as cdk
from aws_cdk import (
    Stack, Duration,
    aws_ec2 as ec2,
    aws_iam as iam,
    aws_route53 as route53,
    aws_cognito as cognito,
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

        repo_url = "https://github.com/d-abhishek/mcp-prompt-library.git"
        repo_branch = "ec2-deployment"
        domain_name = "xl2-mcp.de"
        domain_name_alt = "www.xl2-mcp.de"
        region = cdk.Stack.of(self).region

        # 1) VPC (use default)
        vpc = ec2.Vpc.from_lookup(self, "VPC", is_default=True)

        # 2) Cognito User Pool
        user_pool = cognito.UserPool(
            self, "McpUserPool",
            self_sign_up_enabled=True,
            sign_in_aliases=cognito.SignInAliases(email=True),
            auto_verify=cognito.AutoVerifiedAttrs(email=True),
            mfa=cognito.Mfa.OFF,                        
            password_policy=cognito.PasswordPolicy(
                min_length=8, require_lowercase=False, require_uppercase=False,
                require_digits=False, require_symbols=False
            ),
            removal_policy=cdk.RemovalPolicy.DESTROY,
        )

        user_pool_domain = cognito.UserPoolDomain(
            self, "McpCognitoDomain",
            user_pool=user_pool,
            cognito_domain=cognito.CognitoDomainOptions(
                domain_prefix="xl2-mcp-de"  # unique per region/account
            ),
        )

        resource_server = user_pool.add_resource_server(
            "McpResourceServer",
            identifier=f"https://{domain_name}/mcp",
            user_pool_resource_server_name="MCP URL",
        )

        app_client = user_pool.add_client(
            "McpWebClient",
            auth_flows=cognito.AuthFlow(
                user_srp=True,
                user_password=True,
            ),
            o_auth=cognito.OAuthSettings(
                flows=cognito.OAuthFlows(
                    authorization_code_grant=True
                ),
                scopes=[
                    cognito.OAuthScope.OPENID,
                    cognito.OAuthScope.EMAIL,
                    cognito.OAuthScope.PROFILE,
                ],
                callback_urls=[f"https://{domain_name}/auth/callback"],
                logout_urls=[f"https://{domain_name}/auth/logout"],
            ),
            generate_secret=True,
        )  

        # 3) Security Group with 80, 443, 22, 8000 open
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

        # 3) Hosted zone lookup
        zone = route53.HostedZone.from_lookup(self, "Zone", domain_name=domain_name)

        # 4) Instance role with Route53 permissions for DNS-01 (dns_aws)
        role = iam.Role(self, "McpRole", assumed_by=iam.ServicePrincipal("ec2.amazonaws.com")) # type: ignore
        role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSSMManagedInstanceCore"))
        role.add_to_policy(iam.PolicyStatement(
            actions=["route53:ListHostedZones","route53:ListHostedZonesByName","route53:ListResourceRecordSets"],
            resources=["*"],
        ))
        role.add_to_policy(iam.PolicyStatement(
            actions=["route53:ChangeResourceRecordSets"],
            resources=[f"arn:aws:route53:::hostedzone/{zone.hosted_zone_id}"],
        ))
        role.add_to_policy(iam.PolicyStatement(
            actions=["route53:GetChange"],
            resources=["arn:aws:route53:::change/*"],
        ))
        role.add_to_policy(iam.PolicyStatement(
            actions=["cognito-idp:DescribeUserPoolClient"],
            resources=["*"],
        ))

        # 5) EC2 Instance
        user_data = ec2.UserData.for_linux()
        user_data.add_commands(
            # ===== System prep =====
            "set -euxo pipefail",
            "sudo dnf -y update",
            "sudo dnf -y install python3.13 python3.13-pip git cronie socat nginx awscli",
            "sudo systemctl enable --now crond nginx",

            # ===== App dir + venv =====
            "sudo install -o ec2-user -g ec2-user -d /opt/mcp",
            "cd /opt/mcp",
            "python3.13 -m venv venv",
            "source venv/bin/activate",
            "python -m pip install --upgrade pip",

            # === Fetch Cognito App Client Secret (may return 'None' if no secret) ===
            f"CLIENT_SECRET=$(aws cognito-idp describe-user-pool-client "
            f"  --region {region} "
            f"  --user-pool-id {user_pool.user_pool_id} "
            f"  --client-id {app_client.user_pool_client_id} "
            f"  --query 'UserPoolClient.ClientSecret' --output text 2>/dev/null || true)",
            # normalize "None" → empty
            'if [ "$CLIENT_SECRET" = "None" ] || [ "$CLIENT_SECRET" = "null" ]; then CLIENT_SECRET=""; fi',

            # === Write /opt/mcp/.env for the app ===
            "sudo tee /opt/mcp/.env >/dev/null <<EOF",
            f"USER_POOL_ID={user_pool.user_pool_id}",
            f"AWS_REGION={region}",
            f"CLIENT_ID={app_client.user_pool_client_id}",
            "CLIENT_SECRET=${CLIENT_SECRET}",
            f"BASE_URL=https://{domain_name}",
            "EOF",
            "sudo chown ec2-user:ec2-user /opt/mcp/.env",
            "sudo chmod 600 /opt/mcp/.env",

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

            # ===== ACME via Route53 (dns_aws) as ec2-user =====

            # Install acme.sh for ec2-user and issue cert for your domain
            f"sudo -u ec2-user -i bash -lc 'set -euo pipefail; "
            "curl -fsSL https://get.acme.sh | sh -s email=hhn.thesis@gmail.com; "
            "set +u; . ~/.acme.sh/acme.sh.env; set -u; "
            "~/.acme.sh/acme.sh --set-default-ca --server letsencrypt; "
            # # persist the zone id for dns_aws (prevents ambiguity)
            # f"echo \"export AWS_HOSTED_ZONE_ID=\\\"{zone.hosted_zone_id}\\\"\" >> ~/.acme.sh/account.conf; "
            # Issue for apex + www (drop the -d for www if you don't need it)
            f"~/.acme.sh/acme.sh --issue --dns dns_aws -d \"{domain_name}\" -d \"{domain_name_alt}\" --dnssleep 120 --debug 2"
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
            f"  server_name {domain_name} {domain_name_alt};",
            "  return 301 https://$host$request_uri;",
            "}",
            "",
            "server {",
            "  listen 443 ssl http2;",
            f"  server_name {domain_name} {domain_name_alt};",
            "",
            f"  ssl_certificate     /etc/nginx/ssl/{domain_name}/fullchain.pem;",
            f"  ssl_certificate_key /etc/nginx/ssl/{domain_name}/privkey.pem;",
            "",
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
            role=role, # type: ignore
        )

        # 6) Elastic IP + association (stable public IP)
        eip = ec2.CfnEIP(self, "McpEip")
        ec2.CfnEIPAssociation(
            self, "McpEipAssoc",
            eip=eip.ref,
            instance_id=instance.instance_id,
        )

        # 7) A records to EIP (root + www)
        route53.ARecord(
            self, "RootA",
            zone=zone,
            record_name=domain_name,   # apex
            target=route53.RecordTarget.from_ip_addresses(eip.attr_public_ip),
            ttl=Duration.minutes(1),
        )
        route53.ARecord(
            self, "WwwA",
            zone=zone,
            record_name=f"www.{domain_name}",
            target=route53.RecordTarget.from_ip_addresses(eip.attr_public_ip),
            ttl=Duration.minutes(1),
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
        cdk.CfnOutput(self, "CognitoUserPoolId", value=user_pool.user_pool_id)
        cdk.CfnOutput(self, "CognitoClientId", value=app_client.user_pool_client_id)
        cdk.CfnOutput(self, "CognitoHostedUiBase", value=user_pool_domain.base_url())
        # Example authorize URL (for testing)
        cdk.CfnOutput(
            self, "AuthorizeUrlExample",
            value=f"{user_pool_domain.base_url()}/oauth2/authorize?client_id={app_client.user_pool_client_id}&response_type=code&scope=openid+email+profile&redirect_uri=https%3A%2F%2F{domain_name}%2Fauth%2Fcallback"
        )