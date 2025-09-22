# backend/agents/critic.py
from .base import Agent

class CriticAgent(Agent):
    """
    An agent that critiques a summary based on the original research.
    """
    def run(self, context: str) -> str:
        system_prompt = (
            "You are a meticulous critic. Your role is to analyze a summary and the original "
            "research material it was based on. Check for inconsistencies, missing key points, "
            "or potential bias in the summary. Provide your feedback as a concise list of "
            "actionable points for improvement. If the summary is good, state that clearly."
            "\nExample Output:\n"
            "- The summary missed the point about X from the research.\n"
            "- The tone seems slightly biased towards Y; rephrase for neutrality.\n"
            "- The point about Z is well-summarized and accurate."
        )
        
        user_prompt = (
            "Please critique the following summary based on the provided research context."
            f"\n\n{context}"
        )

        prompt = self._create_prompt(system_prompt, user_prompt)
        critique = self._get_completion(prompt)
        return critique