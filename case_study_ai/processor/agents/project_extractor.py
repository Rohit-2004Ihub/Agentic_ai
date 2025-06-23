from langchain_core.runnables import Runnable
from .utils import get_llm
from langchain_core.prompts import PromptTemplate

template = """
You will extract a structured summary from the following project metadata.

Project Metadata:
{input}

Return a dictionary with: title, problem, goal, tech_stack, target_users, and outcome.
"""

prompt = PromptTemplate.from_template(template)
llm = get_llm()

project_extractor_agent: Runnable = prompt | llm
from langchain_core.runnables import Runnable
from .utils import get_llm
from langchain_core.prompts import PromptTemplate

template = """
You will extract a structured summary from the following project metadata.

Project Metadata:
{input}

Return a dictionary with: title, problem, goal, tech_stack, target_users, and outcome.
"""

prompt = PromptTemplate.from_template(template)
llm = get_llm()

project_extractor_agent: Runnable = prompt | llm


