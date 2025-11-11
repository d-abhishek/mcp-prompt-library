# server/server.py
import os
from pathlib import Path
from dotenv import load_dotenv

from fastmcp import FastMCP
from .prompt_registry import register_prompts
from .tool_registry import register_tools

from fastmcp.server.auth.providers.aws import AWSCognitoProvider

# Load .env from repo root (optional)
ENV_FILE = Path(__file__).resolve().parent.parent / ".env"
if ENV_FILE.exists():
    load_dotenv(ENV_FILE)

# Check if running in local testing mode
LOCAL_TESTING = os.getenv("LOCAL_TESTING", "false").lower() == "true"

# Conditionally configure authentication
if LOCAL_TESTING:
    # Local testing mode: No authentication required
    print("⚠️  Running in LOCAL_TESTING mode - Authentication and Authorization are DISABLED")
    mcp = FastMCP(name="mcp-prompt-library", auth=None)
else:
    # Production mode: Full Cognito authentication
    auth_provider = AWSCognitoProvider(
        user_pool_id=os.environ["USER_POOL_ID"],   # Your AWS Cognito user pool ID
        aws_region=os.environ["AWS_REGION"],               # AWS region (defaults to eu-central-1)
        client_id=os.environ["CLIENT_ID"],          # Your app client ID
        client_secret=os.environ["CLIENT_SECRET"],  # Your app client Secret
        base_url=os.environ["BASE_URL"],        # Must match your callback URL
        # redirect_path="/auth/callback"         # Default value, customize if needed
    )
    mcp = FastMCP(name="mcp-prompt-library", auth=auth_provider)

register_tools(mcp)
register_prompts(mcp)

# Expose ASGI app at /mcp
app = mcp.http_app()

# Health endpoint for checks
from starlette.responses import JSONResponse  # noqa: E402
@mcp.custom_route("/health", methods=["GET"])
async def health(_):
    return JSONResponse({"status": "healthy"})
