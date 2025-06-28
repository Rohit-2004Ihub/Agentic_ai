from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import Runnable
from .utils import get_llm

template = """
Based on the following case study, suggest appropriate visuals such as architecture diagrams, user flows, or charts.

Then generate a Mermaid flowchart (flowchart TD format) **as plain text only**, without wrapping it in markdown code blocks (no triple backticks or markdown).

Format:
Visual Suggestions:
[Write your visual suggestions here.]

Mermaid Flowchart:
Start your flowchart directly with "flowchart TD" and write each step in plain Mermaid syntax.

Case Study:
{case_study}
"""


prompt = PromptTemplate.from_template(template)
visual_recommender_agent: Runnable = prompt | get_llm()
