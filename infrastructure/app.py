#!/usr/bin/env python3
import os

import aws_cdk as cdk

from cdk.mcp_stack import McpCdkStack

app = cdk.App()

account = os.getenv("CDK_DEFAULT_ACCOUNT")
region  = os.getenv("CDK_DEFAULT_REGION")

McpCdkStack(app, "McpServerStack",
        env=cdk.Environment(account=account, region=region),
)

app.synth()
