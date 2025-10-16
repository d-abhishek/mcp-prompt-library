#!/bin/bash
set -e

echo "Starting MCP Prompt Library server..."
echo "Working directory: $(pwd)"
echo "Python path: $PYTHONPATH"
echo "PATH: $PATH"

# Test imports first
echo "Testing imports..."
/usr/bin/python3.13 -c "import fastmcp, starlette, uvicorn; print('✅ Imports OK')"

# Start the server
echo "Starting uvicorn server..."
exec /usr/bin/python3.13 -m uvicorn server.server:asgi_app --host 127.0.0.1 --port 8000 --log-level debug