
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from pathlib import Path
import os
import json 

from .orchestrator import Orchestrator

print("--- [STARTUP] Attempting to load .env file ---")
dotenv_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=dotenv_path)
print(f"--- [STARTUP] .env file exists: {dotenv_path.exists()}")
# Now, let's check if the key was actually loaded.
api_key_check = os.getenv("OPENAI_API_KEY")
print(f"--- [STARTUP] OPENAI_API_KEY is loaded: {api_key_check is not None}")

app = FastAPI(
    title="Mini Agent Workflow Orchestrator",
    description="An API for running collaborative AI agent workflows.",
    version="0.1.0"
)

# --- Initialize the Orchestrator ---
# Construct the path to the configuration file
CONFIG_PATH = Path(__file__).parent / "config" / "workflow.json"
orchestrator = Orchestrator(config_path=CONFIG_PATH)

# Pydantic models for request and response validation
class WorkflowRequest(BaseModel):
    query: str
    
class WorkflowResponse(BaseModel):
    final_output: str
    workflow_log: list

@app.get("/")
def read_root():
    return {"message": "Welcome to the Mini Agent Workflow Orchestrator API"}

@app.post("/run-workflow", response_model=WorkflowResponse)
def run_workflow_endpoint(request: WorkflowRequest) -> WorkflowResponse:
    """
    Receives a query and runs it through the workflow defined in workflow.json.
    """
    result = orchestrator.run_workflow(request.query)
    return result

@app.get("/get-workflow-config")
def get_workflow_config():
    """
    An endpoint to provide the frontend with the current workflow structure.
    """
    with open(CONFIG_PATH, 'r') as f:
        config_data = json.load(f)
    return {"name": config_data.get("name"), "steps": config_data.get("steps")}