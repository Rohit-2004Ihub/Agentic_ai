from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .utils.docx_reader import extract_text_from_docx
from .agents.agent_executor import agent_executor
from google.api_core.exceptions import ResourceExhausted
import traceback

@csrf_exempt
def process_project_docx(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=405)

    uploaded_file = request.FILES.get("file")
    if not uploaded_file:
        return JsonResponse({"error": "No file uploaded"}, status=400)

    try:
        # Extract and limit input text
        raw_text = extract_text_from_docx(uploaded_file)
        print("📄 Extracted Text Preview:", raw_text[:500])

        if len(raw_text) > 12000:
            raw_text = raw_text[:12000] + "\n\n...[Truncated]"

        input_prompt = f"""
        I have a project document. Please process it through multiple agents:
        1. Extract a structured summary.
        2. Compose a case study.
        3. Refine the case using RAG.
        4. Recommend visual aids.
        5. Simulate the pitch.

        Project content:
        {raw_text}
        """

        # Run full LangChain executor
        result = agent_executor.invoke({"input": input_prompt})

        # Parse intermediate steps
        steps = result.get("intermediate_steps", [])
        structured = case_study = refined = visuals = pitch = ""

        for action, observation in steps:
            tool = action.tool
            output = str(observation)

            if tool == "ProjectExtractor":
                structured = output
            elif tool == "CaseStudyComposer":
                case_study = output
            elif tool == "RAGRefiner":
                refined = output
            elif tool == "VisualAidRecommender":
                visuals = output
            elif tool == "PitchSimulator":
                pitch = output

        final_summary = str(result.get("output", ""))

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

    except ResourceExhausted:
        return JsonResponse({"error": "🧠 Gemini API quota exceeded. Please wait or upgrade your quota."}, status=429)

    except Exception as e:
        traceback.print_exc()
        return JsonResponse({"error": str(e)}, status=500)
