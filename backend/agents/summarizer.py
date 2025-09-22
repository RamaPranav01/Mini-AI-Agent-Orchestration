# backend/agents/summarizer.py
from .base import Agent

class SummarizerAgent(Agent):
    """
    An agent that summarizes text.
    """
    def run(self, input_data: str) -> str:
        system_prompt = (
            "You are an expert summarizer. Your goal is to take the provided research text "
            "and distill it into a concise, neutral, and easy-to-read summary. "
            "Focus on the key points and present them clearly."
        )
        
        user_prompt = f"Please summarize the following text:\n\n{input_data}"

        prompt = self._create_prompt(system_prompt, user_prompt)
        summary = self._get_completion(prompt)
        return summary