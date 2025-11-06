#!/usr/bin/env python3
import os

import aws_cdk as cdk

from cdk.cdk_stack import CdkStack
from cdk.mcp_stack import McpCdkStack

app = cdk.App()

account = os.getenv("CDK_DEFAULT_ACCOUNT")
region  = os.getenv("CDK_DEFAULT_REGION")

CdkStack(app, "McpInfraStack",
        env=cdk.Environment(account=account, region=region),
)
McpCdkStack(app, "McpServerStack",
        env=cdk.Environment(account=account, region=region),
)

app.synth()
