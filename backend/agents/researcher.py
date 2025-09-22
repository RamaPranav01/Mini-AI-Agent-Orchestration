# backend/agents/researcher.py
from .base import Agent

class ResearcherAgent(Agent):
    """
    An agent that performs research on a given topic.
    For this mini-project, it simulates research by generating key facts and sources
    based on the LLM's internal knowledge.
    """
    def run(self, topic: str) -> str:
        system_prompt = (
            "You are a world-class researcher. Your task is to find relevant information, "
            "key facts, and arguments on a given topic. Do not write a summary. "
            "Instead, provide a structured list of bullet points covering the main aspects, "
            "including different viewpoints. Base this on your internal knowledge."
            "\nExample Output:\n"
            "- Point 1 about the topic.\n"
            "- Point 2 with a different perspective.\n"
            "- Statistic or key fact related to the topic."
        )
        
        user_prompt = f"Please conduct research on the following topic: {topic}"

        prompt = self._create_prompt(system_prompt, user_prompt)
        research_data = self._get_completion(prompt)
        return research_data