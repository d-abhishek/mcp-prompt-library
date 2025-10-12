"""
Stateless Python Lambda handler for MCP Streamable HTTP.
"""

import json
import logging
import traceback
from typing import Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def handler(event, context):
    """
    AWS Lambda handler that processes MCP requests in a stateless manner.
    Each request creates a fresh MCP server instance, processes the request, and returns.
    """
    logger.info(f"Received event: {json.dumps(event, default=str)}")
    
    try:
        # Handle CORS preflight
        if event.get('httpMethod') == 'OPTIONS':
            return cors_response(200, {})
        
        # Extract MCP request from API Gateway event
        mcp_request = extract_mcp_request(event)
        if not mcp_request:
            return cors_response(400, {
                "jsonrpc": "2.0",
                "id": None,
                "error": {
                    "code": -32700,
                    "message": "Parse error: No request body"
                }
            })
        
        # Process the MCP request
        response = process_mcp_request(mcp_request)
        
        # Return successful response
        return cors_response(200, response)
        
    except Exception as e:
        logger.error(f"Error processing request: {e}")
        logger.error(traceback.format_exc())
        
        return cors_response(500, {
            "jsonrpc": "2.0",
            "id": None,
            "error": {
                "code": -32603,
                "message": "Internal error",
                "data": str(e)
            }
        })

def cors_response(status_code: int, body: Dict[str, Any]) -> Dict[str, Any]:
    """Create a CORS-enabled API Gateway response"""
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type, Authorization, Accept',
            'Access-Control-Allow-Methods': 'GET, POST, OPTIONS'
        },
        'body': json.dumps(body)
    }

def extract_mcp_request(event: Dict[str, Any]) -> Dict[str, Any]:
    """Extract MCP request from API Gateway event"""
    body = event.get('body')
    if not body:
        return {}
    
    # Handle base64 encoding
    if event.get('isBase64Encoded'):
        import base64
        body = base64.b64decode(body).decode('utf-8')
    
    try:
        request = json.loads(body)
        
        # Validate JSON-RPC 2.0 format
        if request.get('jsonrpc') != '2.0':
            raise ValueError("Invalid JSON-RPC 2.0 request")
        
        return request
        
    except (json.JSONDecodeError, ValueError) as e:
        logger.error(f"Invalid request body: {e}")
        raise

def process_mcp_request(request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Process MCP request in a stateless manner.
    Creates a fresh MCP server instance for each request.
    """
    method = request.get('method')
    params = request.get('params', {})
    request_id = request.get('id')
    
    logger.info(f"Processing MCP method: {method}")
    
    try:
        if method == 'initialize':
            return handle_initialize(request_id)
        elif method == 'ping':
            return handle_ping(request_id)
        elif method == 'prompts/list':
            return handle_prompts_list(request_id)
        elif method == 'prompts/get':
            return handle_prompts_get(request_id, params)
        elif method == 'tools/list':
            return handle_tools_list(request_id)
        elif method == 'tools/call':
            return handle_tools_call(request_id, params)
        else:
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {
                    "code": -32601,
                    "message": f"Method '{method}' not found"
                }
            }
            
    except Exception as e:
        logger.error(f"Error processing method {method}: {e}")
        logger.error(traceback.format_exc())
        
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {
                "code": -32603,
                "message": "Internal error",
                "data": str(e)
            }
        }

def handle_initialize(request_id) -> Dict[str, Any]:
    """Handle MCP initialize request"""
    return {
        "jsonrpc": "2.0",
        "id": request_id,
        "result": {
            "protocolVersion": "2024-11-05",
            "capabilities": {
                "prompts": {
                    "listChanged": True
                },
                "tools": {
                    "listChanged": True
                }
            },
            "serverInfo": {
                "name": "mcp-prompt-library",
                "version": "1.0.0"
            }
        }
    }

def handle_ping(request_id) -> Dict[str, Any]:
    """Handle ping request"""
    return {
        "jsonrpc": "2.0",
        "id": request_id,
        "result": {
            "status": "pong"
        }
    }

def handle_prompts_list(request_id) -> Dict[str, Any]:
    """Handle prompts/list request"""
    try:
        # Import and get prompts in a stateless way
        prompts = get_available_prompts()
        
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "prompts": prompts
            }
        }
    except Exception as e:
        logger.error(f"Error listing prompts: {e}")
        raise

def handle_prompts_get(request_id, params) -> Dict[str, Any]:
    """Handle prompts/get request"""
    prompt_name = params.get('name')
    prompt_args = params.get('arguments', {})
    
    if not prompt_name:
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {
                "code": -32602,
                "message": "Missing prompt name"
            }
        }
    
    try:
        # Execute prompt in a stateless way
        result = execute_prompt(prompt_name, prompt_args)
        
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "messages": [
                    {
                        "role": "user",
                        "content": {
                            "type": "text",
                            "text": result
                        }
                    }
                ]
            }
        }
    except Exception as e:
        logger.error(f"Error executing prompt {prompt_name}: {e}")
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {
                "code": -32602,
                "message": f"Prompt '{prompt_name}' execution failed: {str(e)}"
            }
        }

def handle_tools_list(request_id) -> Dict[str, Any]:
    """Handle tools/list request"""
    try:
        # Import and get tools in a stateless way
        tools = get_available_tools()
        
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "tools": tools
            }
        }
    except Exception as e:
        logger.error(f"Error listing tools: {e}")
        raise

def handle_tools_call(request_id, params) -> Dict[str, Any]:
    """Handle tools/call request"""
    tool_name = params.get('name')
    tool_args = params.get('arguments', {})
    
    if not tool_name:
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {
                "code": -32602,
                "message": "Missing tool name"
            }
        }
    
    try:
        # Execute tool in a stateless way
        result = execute_tool(tool_name, tool_args)
        
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "content": [
                    {
                        "type": "text",
                        "text": str(result)
                    }
                ]
            }
        }
    except Exception as e:
        logger.error(f"Error executing tool {tool_name}: {e}")
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {
                "code": -32602,
                "message": f"Tool '{tool_name}' execution failed: {str(e)}"
            }
        }

def get_available_prompts():
    """Get list of available prompts in a stateless way"""
    try:
        import os
        import frontmatter
        
        prompts = []
        prompts_dir = "/var/task/prompts"  # Lambda task directory
        
        if not os.path.exists(prompts_dir):
            prompts_dir = "prompts"  # Fallback for local testing
            
        if os.path.exists(prompts_dir):
            for filename in os.listdir(prompts_dir):
                if filename.endswith('.md'):
                    filepath = os.path.join(prompts_dir, filename)
                    with open(filepath, 'r', encoding='utf-8') as f:
                        post = frontmatter.load(f)
                        
                    prompt_name = post.metadata.get('name', filename[:-3])
                    prompts.append({
                        "name": prompt_name,
                        "description": post.metadata.get('description', ''),
                        "arguments": post.metadata.get('arguments', [])
                    })
        
        return prompts
        
    except Exception as e:
        logger.error(f"Error getting prompts: {e}")
        return []

def get_available_tools():
    """Get list of available tools in a stateless way"""
    # For now, return empty list - tools can be implemented later
    return []

def execute_prompt(prompt_name: str, args: Dict[str, Any]) -> str:
    """Execute a prompt in a stateless way"""
    try:
        import os
        import frontmatter
        from jinja2 import Template
        
        prompts_dir = "/var/task/prompts"  # Lambda task directory
        if not os.path.exists(prompts_dir):
            prompts_dir = "prompts"  # Fallback for local testing
            
        filepath = os.path.join(prompts_dir, f"{prompt_name}.md")
        
        if not os.path.exists(filepath):
            raise ValueError(f"Prompt '{prompt_name}' not found")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            post = frontmatter.load(f)
        
        # Render the prompt template with arguments
        template = Template(post.content)
        result = template.render(**args)
        
        return result
        
    except Exception as e:
        logger.error(f"Error executing prompt {prompt_name}: {e}")
        raise

def execute_tool(tool_name: str, args: Dict[str, Any]) -> str:
    """Execute a tool in a stateless way"""
    # Tools implementation can be added here
    raise ValueError(f"Tool '{tool_name}' not implemented")