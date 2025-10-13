from typing import cast
from aws_cdk import (
    Duration,
    Stack,
    CfnOutput,
    Fn,
    aws_apigateway as apigw,
    aws_lambda as _lambda,
    aws_ec2 as ec2,
    aws_iam as iam,
)
from constructs import Construct

class McpPrivateApiStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # ──────────────────────────────────────────────────────────────────────
        # 1) VPC (public + isolated subnets; no NAT needed for private API)
        # ──────────────────────────────────────────────────────────────────────
        vpc = ec2.Vpc(
            self, 
            "McpVpc",
            max_azs=1,
            nat_gateways=0,  # No NAT gateways for cost efficiency and since internet access is not needed
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name="PublicSubnet",
                    subnet_type=ec2.SubnetType.PUBLIC,
                    cidr_mask=24
                ),
                ec2.SubnetConfiguration(
                    name="IsolatedSubnet",
                    subnet_type=ec2.SubnetType.PRIVATE_ISOLATED,
                    cidr_mask=24
                )
            ]
        )

        # Security Group for the VPC Endpoint (allow HTTPS from within VPC)
        vpce_sg = ec2.SecurityGroup(
            self,
            "McpVpceSg",
            vpc=vpc,
            allow_all_outbound=True,
            description="Security group for API Gateway VPC Endpoint"
        )
        # Allow 443 from VPC CIDR (you can restrict to specific SGs or subnets later)
        # VPC Endpoint and resource policy commented out for public API
        # Uncomment if you need private API Gateway
        
        # vpce_sg.add_ingress_rule(
        #     peer=ec2.Peer.ipv4(vpc.vpc_cidr_block),
        #     connection=ec2.Port.tcp(443),
        #     description="Allow HTTPS traffic from within the VPC"
        # )

        # vpce = ec2.InterfaceVpcEndpoint(
        #     self,
        #     "McpApiVpcEndpoint",
        #     vpc=vpc,
        #     service=ec2.InterfaceVpcEndpointAwsService.APIGATEWAY,
        #     private_dns_enabled=True,
        #     security_groups=[vpce_sg],
        #     subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC)
        # )

        # any_principal: iam.IPrincipal = cast(iam.IPrincipal, iam.AnyPrincipal())
        # deny_stmt = iam.PolicyStatement(
        #     effect=iam.Effect.DENY,
        #     actions=["execute-api:Invoke"],
        #     principals=[any_principal],
        #     resources=["*"],
        #     conditions={"StringNotEquals": {"aws:SourceVpce": vpce.vpc_endpoint_id}},
        # )
        # allow_stmt = iam.PolicyStatement(
        #     effect=iam.Effect.ALLOW,
        #     actions=["execute-api:Invoke"],
        #     principals=[any_principal],
        #     resources=["*"],
        #     conditions={"StringEquals": {"aws:SourceVpce": vpce.vpc_endpoint_id}},
        # )
        # api_policy = iam.PolicyDocument(statements=[deny_stmt, allow_stmt])

        # ──────────────────────────────────────────────────────────────────────
        # 4) Lambda function (Python 3.13) — Python adapter spawning MCP server subprocess
        #    The zip contains lambda_function.py with subprocess bridge to server module
        # ──────────────────────────────────────────────────────────────────────
        lambda_fn = _lambda.Function(
            self,
            "McpLambda",
            runtime=_lambda.Runtime.PYTHON_3_13,
            architecture=_lambda.Architecture.ARM_64,
            handler="lambda_function.handler",  # Python handler that spawns server subprocess
            code=_lambda.Code.from_asset("../mcp-prompt-library.zip"),
            memory_size=2048,
            timeout=Duration.seconds(29),  # API Gateway max timeout is 29 seconds
            description="Python Lambda adapter for MCP server via subprocess",
        )
        
        fn: _lambda.IFunction = cast(_lambda.IFunction, lambda_fn) 

        # ──────────────────────────────────────────────────────────────────────
        # 5) Public REST API Gateway (proxy integration -> Lambda)
        # ──────────────────────────────────────────────────────────────────────
        api = apigw.RestApi(
            self,
            "McpPublicApi",
            rest_api_name="mcp-public",
            endpoint_configuration=apigw.EndpointConfiguration(
                types=[apigw.EndpointType.REGIONAL],  # Changed to PUBLIC
            ),
            deploy_options=apigw.StageOptions(stage_name="prod"),
            cloud_watch_role=True,
            description="Public API Gateway for FastMCP Lambda"
            # Removed resource policy - not needed for public endpoint
        )

        lambda_integration = apigw.LambdaIntegration(fn, proxy=True)

        # Proxy ALL requests to Lambda (let FastMCP handle routing)
        api.root.add_proxy(
            default_integration=lambda_integration,
            any_method=True
        )

        # ──────────────────────────────────────────────────────────────────────
        # 6) Useful Outputs
        # ──────────────────────────────────────────────────────────────────────
        CfnOutput(self, "RestApiId", value=api.rest_api_id)
        # CfnOutput(self, "VpcEndpointId", value=vpce.vpc_endpoint_id)  # Not needed for public API
        CfnOutput(
            self,
            "ApiInvokeUrl",
            value=f"https://{api.rest_api_id}.execute-api.{self.region}.amazonaws.com/prod/",
            description="Public API Gateway invoke URL - accessible from anywhere",
        )
        #CfnOutput(
        #    self,
        #    "VpcEndpointDns",
        #    value=Fn.select(0, vpce.vpc_endpoint_dns_entries),
        #    description="VPC Endpoint DNS name - use this from EC2 in the VPC",
        #)