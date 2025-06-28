from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import Runnable
from .utils import get_llm

template = """
Simulate pitch feedback. Analyze clarity, impact, innovation, and persuasion.
Give a pitch score (out of 10) and suggestions for improvement.

Input:
{case_study}

Return in plain text with no special characters or markdown formatting.
Format:
Score out of 10
Strengths
Suggestions for Improvement
"""

prompt = PromptTemplate.from_template(template)
pitch_simulator_agent: Runnable = prompt | get_llm()
