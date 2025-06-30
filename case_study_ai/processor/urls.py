from django.urls import path
from .views import process_project_docx, get_user_history, signup_view, login_view

urlpatterns = [
    path("process-docx/", process_project_docx),
    path("user-history/", get_user_history),
    path("signup/", signup_view),
    path("login/", login_view),
]
