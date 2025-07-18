from langchain.tools import Tool
from .project_extractor import project_extractor_agent
from .case_study_composer import case_study_composer_agent
from .visual_recommender import visual_recommender_agent
from .pitch_simulator import pitch_simulator_agent
from .rag_benchmark import rag_benchmark_agent

tools = [
    Tool(
        name="ProjectExtractor",
        func=lambda input: project_extractor_agent.invoke({"input": input}),
        description="Extract a structured project summary from raw text."
    ),
    Tool(
        name="CaseStudyComposer",
        func=lambda input: case_study_composer_agent.invoke({"summary": input}),
        description="Generate a formal case study from structured project summary."
    ),
    Tool(
        name="RAGRefiner",
        func=lambda input: rag_benchmark_agent.invoke({"query": input})["result"],
        description="Refine and benchmark the case study with external knowledge."
    ),
    Tool(
        name="VisualAidRecommender",
        func=lambda input: visual_recommender_agent.invoke({"case_study": input}),
        description="Suggest diagrams and visual aids for the case study."
    ),
    Tool(
        name="PitchSimulator",
        func=lambda input: pitch_simulator_agent.invoke({"case_study": input}),
        description="Evaluate the pitch and provide feedback with a score."
    )
]
