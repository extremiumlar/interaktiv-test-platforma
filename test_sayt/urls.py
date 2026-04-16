from django.urls import path

from .views import get_questions, index, submit_answers

urlpatterns = [
    path("", index, name="home"),
    path("api/questions/", get_questions, name="get_questions"),
    path("api/submit/", submit_answers, name="submit_answers"),
]
