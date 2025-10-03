import asyncio
import os
import json
from typing import List, Dict, Any
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
import httpx
import uvicorn
from pydantic import BaseModel

app = FastAPI(title="TELOS MCP Server", version="1.0.0")

class MCPRequest(BaseModel):
    method: str
    params: Dict[str, Any] = {}

class MCPResponse(BaseModel):
    result: Any = None
    error: Dict[str, Any] = None

# Load TELOS context from GitHub or local file
async def load_telos_context():
    """Load TELOS context from GitHub repository or local file"""
    github_token = os.getenv("GITHUB_TOKEN")
    telos_repo = os.getenv("TELOS_REPO", "your-username/personal-context")
    
    if github_token:
        # Load from GitHub
        async with httpx.AsyncClient() as client:
            try:
                url = f"https://api.github.com/repos/{telos_repo}/contents/telos.md"
                headers = {"Authorization": f"token {github_token}"}
                response = await client.get(url, headers=headers)
                
                if response.status_code == 200:
                    data = response.json()  
                    import base64
                    content = base64.b64decode(data["content"]).decode("utf-8")
                    return content
            except Exception as e:
                print(f"Error loading from GitHub: {e}")
    
    # Fallback to local file
    try:
        with open("/app/context/telos.md", "r") as f:
            return f.read()
    except FileNotFoundError:
        return "# TELOS Context\nNo personal context loaded. Please set up your TELOS file."

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "telos-mcp"}

@app.post("/mcp")
async def mcp_endpoint(request: MCPRequest):
    """Handle MCP requests"""
    if request.method == "tools/list":
        return MCPResponse(result={
            "tools": [
                {
                    "name": "load_telos_context",
                    "description": "Load personal TELOS context for decision filtering",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "request": {
                                "type": "string",
                                "description": "The request to filter through personal context"
                            }
                        }
                    }
                },
                {
                    "name": "apply_telos_filter",
                    "description": "Apply TELOS context to evaluate alignment with personal mission",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "content": {"type": "string", "description": "Content to evaluate"},
                            "decision_type": {"type": "string", "description": "Type of decision"}
                        }
                    }
                }
            ]
        })
    
    elif request.method == "tools/call":
        tool_name = request.params.get("name")
        arguments = request.params.get("arguments", {})
        
        if tool_name == "load_telos_context":
            context = await load_telos_context()
            return MCPResponse(result={"content": context})
            
        elif tool_name == "apply_telos_filter":
            context = await load_telos_context()
            content = arguments.get("content", "")
            
            # Simple TELOS filtering logic
            filtered_response = f"""
            TELOS-Filtered Analysis:
            
            Personal Context Applied: {context[:200]}...
            
            Content Analysis: {content}
            
            Alignment Assessment: [This would contain AI-generated alignment analysis]
            """
            
            return MCPResponse(result={"filtered_content": filtered_response})
    
    else:
        return MCPResponse(error={"code": -32601, "message": f"Method {request.method} not found"})

if __name__ == "__main__":
    port = int(os.getenv("MCP_PORT", 3001))
    uvicorn.run(app, host="0.0.0.0", port=port)