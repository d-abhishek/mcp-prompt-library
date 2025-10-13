#!/usr/bin/env python3
"""
Simplified Python Lambda handler that directly uses the MCP server components
without subprocess complexity.
"""

import json
import logging
import os
import sys
from typing import Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add server to path
sys.path.insert(0, '/var/task/server')
sys.path.insert(0, '/var/task')

def handler(event, context):
    """AWS Lambda handler that directly uses MCP server components"""
    logger.info(f"Received event: {json.dumps(event, default=str)}")
    
    try:
        # Handle CORS preflight
        if event.get('httpMethod') == 'OPTIONS':
            return {
                'statusCode': 200,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
                    'Access-Control-Allow-Headers': 'Content-Type, Authorization',
                    'Access-Control-Max-Age': '86400'
                },
                'body': ''
            }

        # Extract MCP request
        try:
            if event.get('body'):
                mcp_request = json.loads(event['body'])
            else:
                raise ValueError('No request body')
        except (json.JSONDecodeError, ValueError) as e:
            return {
                'statusCode': 400,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Content-Type': 'application/json'
                },
                'body': json.dumps({
                    'jsonrpc': '2.0',
                    'id': None,
                    'error': {
                        'code': -32700,
                        'message': 'Parse error: Invalid JSON'
                    }
                })
            }

        # Process the MCP request directly
        mcp_response = process_mcp_request(mcp_request)

        # Return successful response
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            'body': json.dumps(mcp_response)
        }

    except Exception as e:
        logger.error(f"Error processing request: {e}")
        logger.exception("Full traceback:")
        
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'jsonrpc': '2.0',
                'id': None,
                'error': {
                    'code': -32603,
                    'message': 'Internal error',
                    'data': str(e)
                }
            })
        }

def process_mcp_request(request: Dict[str, Any]) -> Dict[str, Any]:
    """Process MCP request and return response"""
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
                'jsonrpc': '2.0',
                'id': request_id,
                'error': {
                    'code': -32601,
                    'message': f"Method '{method}' not found"
                }
            }
            
    except Exception as e:
        logger.error(f"Error processing method {method}: {e}")
        logger.exception("Full traceback:")
        
        return {
            'jsonrpc': '2.0',
            'id': request_id,
            'error': {
                'code': -32603,
                'message': 'Internal error',
                'data': str(e)
            }
        }

def handle_initialize(request_id) -> Dict[str, Any]:
    """Handle MCP initialize request"""
    return {
        'jsonrpc': '2.0',
        'id': request_id,
        'result': {
            'protocolVersion': '2024-11-05',
            'capabilities': {
                'prompts': {
                    'listChanged': True
                },
                'tools': {
                    'listChanged': True
                }
            },
            'serverInfo': {
                'name': 'mcp-prompt-library',
                'version': '1.0.0'
            }
        }
    }

def handle_ping(request_id) -> Dict[str, Any]:
    """Handle ping request"""
    return {
        'jsonrpc': '2.0',
        'id': request_id,
        'result': {
            'status': 'pong'
        }
    }

def handle_prompts_list(request_id) -> Dict[str, Any]:
    """Handle prompts/list request"""
    try:
        from prompt_handlers import get_available_prompts
        prompts = get_available_prompts()
        
        return {
            'jsonrpc': '2.0',
            'id': request_id,
            'result': {
                'prompts': prompts
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
            'jsonrpc': '2.0',
            'id': request_id,
            'error': {
                'code': -32602,
                'message': 'Missing prompt name'
            }
        }
    
    try:
        from prompt_handlers import execute_prompt
        result = execute_prompt(prompt_name, prompt_args)
        
        return {
            'jsonrpc': '2.0',
            'id': request_id,
            'result': {
                'messages': [
                    {
                        'role': 'user',
                        'content': {
                            'type': 'text',
                            'text': result
                        }
                    }
                ]
            }
        }
    except Exception as e:
        logger.error(f"Error executing prompt {prompt_name}: {e}")
        return {
            'jsonrpc': '2.0',
            'id': request_id,
            'error': {
                'code': -32603,
                'message': f"Error executing prompt: {str(e)}"
            }
        }

def handle_tools_list(request_id) -> Dict[str, Any]:
    """Handle tools/list request"""
    try:
        # Import the tools and get their definitions
        from prompt_tools import get_tool_definitions
        tools = get_tool_definitions()
        
        return {
            'jsonrpc': '2.0',
            'id': request_id,
            'result': {
                'tools': tools
            }
        }
    except Exception as e:
        logger.error(f"Error listing tools: {e}")
        logger.exception("Tools list error:")
        raise

def handle_tools_call(request_id, params) -> Dict[str, Any]:
    """Handle tools/call request"""
    tool_name = params.get('name')
    tool_args = params.get('arguments', {})
    
    if not tool_name:
        return {
            'jsonrpc': '2.0',
            'id': request_id,
            'error': {
                'code': -32602,
                'message': 'Missing tool name'
            }
        }
    
    try:
        from prompt_tools import execute_tool
        result = execute_tool(tool_name, tool_args)
        
        return {
            'jsonrpc': '2.0',
            'id': request_id,
            'result': {
                'content': [
                    {
                        'type': 'text',
                        'text': str(result)
                    }
                ]
            }
        }
    except Exception as e:
        logger.error(f"Error executing tool {tool_name}: {e}")
        return {
            'jsonrpc': '2.0',
            'id': request_id,
            'error': {
                'code': -32603,
                'message': f"Error executing tool: {str(e)}"
            }
        }