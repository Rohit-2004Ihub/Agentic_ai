from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from .utils.docx_reader import extract_text_from_docx
from .agents.agent_executor import agent_executor
from .utils.mongo_client import save_rag_result, collection
import traceback
import re
import json
import pytz
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.views import View


def format_paragraphs(text: str, space_between=True) -> str:
    text = text.replace("**", "")
    text = text.replace("\\n", "\n").replace("\r\n", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{2,}", "\n", text)
    if space_between:
        text = re.sub(r"\n(?=\S)", "\n\n", text)
    return text.strip()


class RegisterView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")

        if User.objects.filter(username=username).exists():
            return JsonResponse({"error": "Username already exists"}, status=400)

        user = User.objects.create_user(username=username, password=password)
        return JsonResponse({"message": "User registered", "user_id": user.id})


@csrf_exempt
def signup_view(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")

        if User.objects.filter(username=username).exists():
            return JsonResponse({"error": "Username already exists"}, status=400)

        user = User.objects.create_user(username=username, password=password)
        return JsonResponse({"message": "Signup successful", "user_id": user.id})

    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def login_view(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return JsonResponse({"message": "Login successful", "user_id": user.id})
        else:
            return JsonResponse({"error": "Invalid credentials"}, status=401)

    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def process_project_docx(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=405)

    uploaded_file = request.FILES.get("file")
    user_id = request.POST.get("user_id")

    if not uploaded_file or not user_id:
        return JsonResponse({"error": "Missing file or user ID"}, status=400)

    try:
        raw_text = extract_text_from_docx(uploaded_file)
        print("📄 Extracted Text Preview:", raw_text[:300])

        input_prompt = f"""
        I have a project document. First extract a structured summary, then generate a case study, 
        refine it with benchmarking, suggest visual aids, and finally simulate the pitch.
        Here is the document content:
        {raw_text}
        """

        result = agent_executor.invoke({"input": input_prompt})
        steps = result.get("intermediate_steps", [])

        structured = case_study = refined = visuals = pitch = ""

        for action, observation in steps:
            tool_name = action.tool
            obs_text = getattr(observation, "content", str(observation))

            if tool_name == "ProjectExtractor":
                structured = format_paragraphs(obs_text)
            elif tool_name == "CaseStudyComposer":
                case_study = format_paragraphs(obs_text)
            elif tool_name == "RAGRefiner":
                refined = format_paragraphs(obs_text)

                save_rag_result(
                    user_id=user_id,
                    document_name=uploaded_file.name,
                    refined_text=refined,
                    metadata={"source": "agent_pipeline", "doc_size": len(raw_text)}
                )
            elif tool_name == "VisualAidRecommender":
                visuals = format_paragraphs(obs_text)
            elif tool_name == "PitchSimulator":
                pitch = format_paragraphs(obs_text)

        final_output = result.get("output", "")
        if hasattr(final_output, "content"):
            final_summary = final_output.content
        elif isinstance(final_output, dict) and "content" in final_output:
            final_summary = final_output["content"]
        else:
            match = re.search(r"content='(.*?)'", str(final_output), re.DOTALL)
            final_summary = match.group(1) if match else str(final_output)

        final_summary_clean = format_paragraphs(final_summary)

        if request.GET.get("plain") == "1":
            return HttpResponse(final_summary_clean, content_type="text/plain")

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


@csrf_exempt
def get_user_history(request):
    if request.method != "GET":
        return JsonResponse({"error": "Invalid request method"}, status=405)

    user_id = request.GET.get("user_id")
    if not user_id:
        return JsonResponse({"error": "Missing user ID"}, status=400)

    try:
        results = collection.find({"user_id": user_id}).sort("timestamp", -1)

        history = []
        for item in results:
            readable_time = item.get("timestamp").astimezone(pytz.timezone("Asia/Kolkata")).strftime("%m/%d/%Y at %I:%M:%S %p")
            history.append({
                "document_name": item.get("document_name"),
                "refined_text": item.get("refined_text", "N/A"),
                "timestamp": readable_time
            })

        return JsonResponse({"history": history})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
