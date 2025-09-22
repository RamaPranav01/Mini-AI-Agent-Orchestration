# backend/agents/base.py
from abc import ABC, abstractmethod
from openai import OpenAI, APIError
import os

class Agent(ABC):
    """
    Abstract base class for all agents.
    It handles the client initialization and the core logic for API calls.
    """
    def __init__(self, model_name: str = "gpt-4o-mini"):
        # Ensure the API key is available
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set.")
        
        self.model_name = model_name
        self.client = OpenAI(api_key=api_key)

    @abstractmethod
    def run(self, input_data: str) -> str:
        """
        The main execution method for the agent. Must be implemented by subclasses.
        """
        pass

    def _create_prompt(self, system_prompt: str, user_prompt: str) -> list:
        """A helper to format messages for the OpenAI API."""
        return [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

    def _get_completion(self, prompt_messages: list) -> str:
        """
        Calls the LLM to get a completion, with robust error handling.
        """
        try:
            print(f"--- Calling LLM for {self.__class__.__name__} ---")
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=prompt_messages,
                temperature=0.7, # A bit of creativity
                max_tokens=1024
            )
            content = response.choices[0].message.content
            if content is None:
                 raise ValueError("Received empty content from API.")
            print(f"--- LLM call successful ---")
            return content
        except APIError as e:
            # Handle API-specific errors (e.g., rate limits, invalid key)
            print(f"Error: OpenAI API error in {self.__class__.__name__}: {e}")
            return f"Error: Could not get a response from the AI. Details: {e}"
        except Exception as e:
            # Handle other potential errors (e.g., network issues)
            print(f"An unexpected error occurred in {self.__class__.__name__}: {e}")
            return f"Error: An unexpected error occurred. Details: {e}"