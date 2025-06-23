# processor/urls.py
from django.urls import path
from .views import process_project_docx

urlpatterns = [
    path("process-docx/", process_project_docx, name="process_project_docx"),
]
