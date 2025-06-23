from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .utils.docx_reader import extract_text_from_docx
from .agents.agent_executor import agent_executor
import traceback

@csrf_exempt
def process_project_docx(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=405)

    uploaded_file = request.FILES.get("file")
    if not uploaded_file:
        return JsonResponse({"error": "No file uploaded"}, status=400)

    try:
        # Step 1: Extract raw text from the uploaded DOCX
        raw_text = extract_text_from_docx(uploaded_file)
        print("📄 Extracted Text Preview:", raw_text[:300])

        # Step 2: Build input prompt
        input_prompt = f"""
        I have a project document. First extract a structured summary, then generate a case study, 
        refine it with benchmarking, suggest visual aids, and finally simulate the pitch.
        Here is the document content:
        {raw_text}
        """

        # Step 3: Run the full agent executor with intermediate steps
        result = agent_executor.invoke({"input": input_prompt})
        steps = result.get("intermediate_steps", [])

        # Step 4: Prepare result fields
        structured = ""
        case_study = ""
        refined = ""
        visuals = ""
        pitch = ""

        for action, observation in steps:
            tool_name = action.tool
            # Safely get only the output text content
            obs_str = observation.content if hasattr(observation, "content") else str(observation)

            if tool_name == "ProjectExtractor":
                structured = obs_str
            elif tool_name == "CaseStudyComposer":
                case_study = obs_str
            elif tool_name == "RAGRefiner":
                refined = obs_str
            elif tool_name == "VisualAidRecommender":
                visuals = obs_str
            elif tool_name == "PitchSimulator":
                pitch = obs_str

        # Step 5: Final combined output
        final_output = result.get("output")
        final_summary = final_output.content if hasattr(final_output, "content") else str(final_output)

        return JsonResponse({
            "result": {
                "structured_summary": structured,
                "case_study": case_study,
                "refined_case_study": refined,
                "visuals": visuals,
                "pitch_feedback": pitch,
                "final_summary": final_summary
            }
        })

    except Exception as e:
        traceback.print_exc()
        return JsonResponse({"error": str(e)}, status=500)
