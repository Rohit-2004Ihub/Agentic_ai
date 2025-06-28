from langchain_core.runnables import Runnable
from .utils import get_llm
from langchain_core.prompts import PromptTemplate

template = """
Extract and format the following project information in clean, readable markdown format with no special characters or dictionary-style syntax.

Project Metadata:
{input}

Return in this format (use plain text, not a dictionary or JSON):

### Title
[project title]

### Problem
[clearly stated problem]

### Goal
[project goal]

### Tech Stack
[List of technologies]

### Target Users
[Who benefits from this]

### Outcome
[Final result or implementation outcome]
"""

prompt = PromptTemplate.from_template(template)
llm = get_llm()

project_extractor_agent: Runnable = prompt | llm
