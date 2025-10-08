from typing import cast
from aws_cdk import (
    Duration,
    Stack,
    CfnOutput,
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
        vpce_sg.add_ingress_rule(
            peer=ec2.Peer.ipv4(vpc.vpc_cidr_block),
            connection=ec2.Port.tcp(443),
            description="Allow HTTPS traffic from within the VPC"
        )

        # ──────────────────────────────────────────────────────────────────────
        # 2) Interface VPC Endpoint for API Gateway (execute-api)
        #    IMPORTANT: callers must live in this same VPC (or connected via TGW/peering/DX/VPN)
        # ──────────────────────────────────────────────────────────────────────

        vpce = ec2.InterfaceVpcEndpoint(
            self,
            "McpApiVpcEndpoint",
            vpc=vpc,
            service=ec2.InterfaceVpcEndpointAwsService.APIGATEWAY,
            private_dns_enabled=True,
            security_groups=[vpce_sg],
            subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_ISOLATED)
        )

        # ──────────────────────────────────────────────────────────────────────
        # 3) Lock the API to ONLY this VPC Endpoint via resource policy
        # ──────────────────────────────────────────────────────────────────────
        any_principal: iam.IPrincipal = cast(iam.IPrincipal, iam.AnyPrincipal())

        deny_stmt = iam.PolicyStatement(
            effect=iam.Effect.DENY,
            actions=["execute-api:Invoke"],
            principals=[any_principal],  # type: Sequence[iam.IPrincipal]
            resources=["*"],  # or [api.arn_for_execute_api("*","*","*")] once api exists
            conditions={"StringNotEquals": {"aws:SourceVpce": vpce.vpc_endpoint_id}},
        )
        allow_stmt = iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            actions=["execute-api:Invoke"],
            principals=[any_principal],
            resources=["*"],
            conditions={"StringEquals": {"aws:SourceVpce": vpce.vpc_endpoint_id}},
        )
        api_policy = iam.PolicyDocument(statements=[deny_stmt, allow_stmt])

        # ──────────────────────────────────────────────────────────────────────
        # 4) Lambda function (Python 3.12) — uses your prebuilt zip
        #    The zip should contain handler.py with: handler = Mangum(asgi_app)
        # ──────────────────────────────────────────────────────────────────────
        lambda_fn = _lambda.Function(
            self,
            "McpLambda",
            runtime=_lambda.Runtime.PYTHON_3_13,
            architecture=_lambda.Architecture.ARM_64,
            handler="lambda-handler.handler",  # module.function
            code=_lambda.Code.from_asset("../server/dist/lambda-handler.zip"),
            memory_size=2048,
            timeout=Duration.seconds(29),  # API Gateway max timeout is 29 seconds
            description="Lambda function running FastMCP ASGI app",
        )
        
        fn: _lambda.IFunction = cast(_lambda.IFunction, lambda_fn) 

        # ──────────────────────────────────────────────────────────────────────
        # 5) Private REST API Gateway (proxy integration -> Lambda)
        # ──────────────────────────────────────────────────────────────────────
        api = apigw.RestApi(
            self,
            "McpPrivateApi",
            rest_api_name="mcp-private",
            endpoint_configuration=apigw.EndpointConfiguration(
                types=[apigw.EndpointType.PRIVATE],
            ),
            deploy_options=apigw.StageOptions(stage_name="prod"),
            cloud_watch_role=True,
            description="Private API Gateway for FastMCP Lambda",
            policy=api_policy
        )

        lambda_integration = apigw.LambdaIntegration(fn, proxy=True)

        #Example routes
        api.root.add_resource("health").add_method("GET", lambda_integration)  # GET /health
        api.root.add_resource("mcp").add_method("POST", lambda_integration)  # POST /mcp

        # ──────────────────────────────────────────────────────────────────────
        # 6) Useful Outputs
        # ──────────────────────────────────────────────────────────────────────
        CfnOutput(self, "RestApiId", value=api.rest_api_id)
        CfnOutput(self, "VpcEndpointId", value=vpce.vpc_endpoint_id)
        CfnOutput(
            self,
            "HintInvokeUrlPattern",
            value="https://{vpce_id}-{hash}.execute-api.{region}.vpce.amazonaws.com/prod/{resource}",
            description="Invoke URL pattern (replace placeholders accordingly)",
        )