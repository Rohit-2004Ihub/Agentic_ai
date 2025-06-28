from langchain_core.prompts import PromptTemplate
from .utils import get_llm
from langchain_core.runnables import Runnable

template = """
Generate a professional case study in the format:

Problem: 
Solution: 
Result:  

Based on this project summary:
{summary}
"""

prompt = PromptTemplate.from_template(template)
llm = get_llm()

case_study_composer_agent: Runnable = prompt | llm
