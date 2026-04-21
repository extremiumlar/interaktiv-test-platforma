from django.urls import path

from .views import get_questions, index, submit_answers, test_page

urlpatterns = [
    path("", index, name="home"),
    path("test/", test_page, name="test_page"),
    path("api/questions/", get_questions, name="get_questions"),
    path("api/submit/", submit_answers, name="submit_answers"),
]
