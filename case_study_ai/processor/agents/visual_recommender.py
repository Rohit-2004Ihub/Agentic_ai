from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import Runnable
from .utils import get_llm

template = """
Based on the following case study, suggest appropriate visuals (like architecture diagrams, user flows, or charts).

Also, generate a flowchart in Mermaid.js syntax (flowchart TD) representing the end-to-end pipeline described in the case study.

Format:
- 📍 Visual Suggestions
- 🛠️ Mermaid Flowchart (in ```mermaid ... ``` block)

Case Study:
{case_study}
"""

prompt = PromptTemplate.from_template(template)
visual_recommender_agent: Runnable = prompt | get_llm()
