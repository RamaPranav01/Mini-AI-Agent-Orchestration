# backend/orchestrator.py
import json
from pathlib import Path

# Import all our agent classes
from .agents.researcher import ResearcherAgent
from .agents.summarizer import SummarizerAgent
from .agents.critic import CriticAgent
from .agents.presenter import PresenterAgent

class Orchestrator:
    """
    Manages the workflow of agents based on a JSON configuration file.
    """
    def __init__(self, config_path: Path):
        self.workflow_config = self._load_config(config_path)
        self.agents = self._initialize_agents()
        print("Orchestrator initialized with workflow:", self.workflow_config.get('name'))

    def _load_config(self, config_path: Path) -> dict:
        """Loads the workflow configuration from a JSON file."""
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: Configuration file not found at {config_path}")
            raise
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON in configuration file at {config_path}")
            raise

    def _initialize_agents(self) -> dict:
        """Initializes all available agent classes."""
        return {
            "Researcher": ResearcherAgent(),
            "Summarizer": SummarizerAgent(),
            "Critic": CriticAgent(),
            "Presenter": PresenterAgent(),
        }

    def _prepare_agent_input(self, step_config: dict, context: dict) -> str:
        """Prepares the input string for an agent based on the context and step config."""
        input_keys = step_config['input_key']
        
        if isinstance(input_keys, str):
            # Single input key
            return context.get(input_keys, "")
        
        elif isinstance(input_keys, list):
            # Multiple input keys, format them into a single string
            formatted_input = []
            for key in input_keys:
                data = context.get(key, f"'{key}' not found in context")
                formatted_input.append(f"--- START OF {key.upper()} ---\n{data}\n--- END OF {key.upper()} ---\n")
            return "\n".join(formatted_input)
        
        return ""

    def run_workflow(self, initial_query: str) -> dict:
        """
        Runs the entire workflow as defined in the configuration file.
        """
        print("--- Starting Workflow ---")
        
        # This context dictionary will hold all the data as the workflow progresses
        context = {"initial_query": initial_query}
        workflow_log = []

        for step_config in self.workflow_config.get("steps", []):
            agent_name = step_config["agent"]
            output_key = step_config["output_key"]
            
            agent = self.agents.get(agent_name)
            if not agent:
                print(f"Warning: Agent '{agent_name}' not found. Skipping step.")
                continue

            # Prepare the input for the current agent
            input_data = self._prepare_agent_input(step_config, context)
            
            print(f"--- Running Step {step_config['step']}: {agent_name} ---")
            
            # Execute the agent
            output_data = agent.run(input_data)
            
            # Update the context with the new data
            context[output_key] = output_data
            
            workflow_log.append({
                "step": step_config['step'],
                "agent": agent_name,
                "input": input_data,
                "output": output_data
            })

        print("--- Workflow Finished ---")

        final_result = {
            "final_output": context.get("final_report", "Workflow did not produce a final report."),
            "workflow_log": workflow_log
        }

        return final_result