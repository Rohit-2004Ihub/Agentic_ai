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
        raw_text = extract_text_from_docx(uploaded_file)
        print("📄 Extracted Text:", raw_text[:300])

        agent_output = agent_executor.invoke({
            "input": f"""
            I have a project document. First extract a structured summary, then generate a case study, 
            refine it with benchmarking, suggest visual aids, and finally simulate the pitch.
            Here is the document content:
            {raw_text}
            """
        })

        # If agent_output is a large string, you can parse sections manually using separators
        # But for now, return everything as one and show in frontend fallback
        return JsonResponse({
            "case_study": agent_output,  # replace with actual values if separated
            "refined_case_study": "",    # enhance later
            "visuals": "",
            "pitch_feedback": ""
        })

    except Exception as e:
        traceback.print_exc()
        return JsonResponse({"error": str(e)}, status=500)
