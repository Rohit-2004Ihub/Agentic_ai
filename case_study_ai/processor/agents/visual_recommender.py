from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import Runnable
from .utils import get_llm

template = """
Based on the following case study, suggest appropriate visuals (like architecture diagram, user flow, charts) and where to place them.

Case Study:
{case_study}
"""

prompt = PromptTemplate.from_template(template)
visual_recommender_agent: Runnable = prompt | get_llm()
