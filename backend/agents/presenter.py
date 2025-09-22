# backend/agents/presenter.py
from .base import Agent

class PresenterAgent(Agent):
    """
    An agent that takes a summary and a critique and generates a final,
    polished report for the end-user.
    """
    def run(self, context: str) -> str:
        system_prompt = (
            "You are a final presenter. Your job is to take a summary and a critique "
            "and synthesize them into a single, polished, and well-structured final report. "
            "Address the points from the critique to improve the summary. The final output "
            "should be ready for a professional audience. Do not mention the critique itself "
            "in the final output; simply incorporate its suggestions to make the summary better."
        )
        
        user_prompt = (
            "Using the following context, please generate the final polished report. "
            "Incorporate the feedback from the critique to improve the initial summary."
            f"\n\n{context}"
        )

        prompt = self._create_prompt(system_prompt, user_prompt)
        final_report = self._get_completion(prompt)
        return final_report