from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from .utils.docx_reader import extract_text_from_docx
from .agents.agent_executor import agent_executor
import traceback
import re

def format_paragraphs(text: str, space_between=True) -> str:
    """
    Cleans LLM output for formatting:
    - Removes markdown symbols
    - Converts newline characters
    - Optionally adds paragraph spacing
    """
    text = text.replace("**", "")
    text = text.replace("\\n", "\n").replace("\r\n", "\n")

    # Normalize spaces and line breaks
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{2,}", "\n", text)

    if space_between:
        text = re.sub(r"\n(?=\S)", "\n\n", text)

    return text.strip()

@csrf_exempt
def process_project_docx(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=405)

    uploaded_file = request.FILES.get("file")
    if not uploaded_file:
        return JsonResponse({"error": "No file uploaded"}, status=400)

    try:
        # Step 1: Extract DOCX text
        raw_text = extract_text_from_docx(uploaded_file)
        print("📄 Extracted Text Preview:", raw_text[:300])

        # Step 2: Build the agent prompt
        input_prompt = f"""
        I have a project document. First extract a structured summary, then generate a case study, 
        refine it with benchmarking, suggest visual aids, and finally simulate the pitch.
        Here is the document content:
        {raw_text}
        """

        # Step 3: Run the LangChain agent executor
        result = agent_executor.invoke({"input": input_prompt})
        steps = result.get("intermediate_steps", [])

        # Step 4: Process each agent output
        structured = ""
        case_study = ""
        refined = ""
        visuals = ""
        pitch = ""

        for action, observation in steps:
            tool_name = action.tool
            obs_text = observation.content if hasattr(observation, "content") else str(observation)

            if tool_name == "ProjectExtractor":
                structured = format_paragraphs(obs_text)
            elif tool_name == "CaseStudyComposer":
                case_study = format_paragraphs(obs_text)
            elif tool_name == "RAGRefiner":
                refined = format_paragraphs(obs_text, space_between=True)
            elif tool_name == "VisualAidRecommender":
                visuals = format_paragraphs(obs_text)
            elif tool_name == "PitchSimulator":
                pitch = format_paragraphs(obs_text)

        # Step 5: Clean the final summary
        final_output = result.get("output")

        # Handle all possible output formats safely
        if hasattr(final_output, "content"):
            final_summary = final_output.content
        elif isinstance(final_output, dict) and "content" in final_output:
            final_summary = final_output["content"]
        else:
            match = re.search(r"content='(.*?)'", str(final_output), re.DOTALL)
            final_summary = match.group(1) if match else str(final_output)

        final_summary_clean = format_paragraphs(final_summary, space_between=True)

        # Step 6: Return plain text if ?plain=1
        if request.GET.get("plain") == "1":
            return HttpResponse(final_summary_clean, content_type="text/plain")

        # Otherwise return structured JSON
        return JsonResponse({
            "result": {
                "structured_summary": structured,
                "case_study": case_study,
                "refined_case_study": refined,
                "visuals": visuals,
                "pitch_feedback": pitch,
                "final_summary": final_summary_clean
            }
        })

    except Exception as e:
        traceback.print_exc()
        return JsonResponse({"error": str(e)}, status=500)
