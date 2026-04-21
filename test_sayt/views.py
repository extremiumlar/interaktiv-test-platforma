import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

from .models import Question


DEFAULT_QUESTIONS = [
    {
        "text": "React'da state nimani boshqaradi?",
        "options": [
            "Komponent ichidagi o'zgaruvchan ma'lumotni",
            "Faqat CSS ranglarini",
            "Serverdagi fayllarni",
            "URL marshrutini avtomatik",
        ],
        "correct_option": "Komponent ichidagi o'zgaruvchan ma'lumotni",
    },
    {
        "text": "Django'da ORM nima vazifa bajaradi?",
        "options": [
            "Ma'lumotlar bazasi bilan obyektlar orqali ishlaydi",
            "Faqat frontend animatsiya yaratadi",
            "Rasm formatlarini siqadi",
            "Brauzer cache'ni tozalaydi",
        ],
        "correct_option": "Ma'lumotlar bazasi bilan obyektlar orqali ishlaydi",
    },
    {
        "text": "Tailwind CSS'ning asosiy afzalligi nima?",
        "options": [
            "Utility class'lar bilan tez dizayn qilish",
            "Django model yaratish",
            "SQL query optimizatsiyasi",
            "Python kodini kompilyatsiya qilish",
        ],
        "correct_option": "Utility class'lar bilan tez dizayn qilish",
    },
    {
        "text": "JavaScript'da async/await nima uchun ishlatiladi?",
        "options": [
            "Asinxron kodni o'qilishi oson tarzda yozish uchun",
            "HTML'ni Python'ga aylantirish uchun",
            "Rang palitrasini tanlash uchun",
            "Fail uploadni bloklash uchun",
        ],
        "correct_option": "Asinxron kodni o'qilishi oson tarzda yozish uchun",
    },
]


def _seed_questions_if_empty():
    if Question.objects.exists():
        return
    Question.objects.bulk_create(
        [
            Question(
                text=question["text"],
                options=question["options"],
                correct_option=question["correct_option"],
            )
            for question in DEFAULT_QUESTIONS
        ]
    )


def index(request):
    return render(request, "test_sayt/index.html")


def test_page(request):
    return render(request, "test_sayt/test.html")


@require_GET
def get_questions(request):
    _seed_questions_if_empty()
    questions = list(Question.objects.all().values("id", "text", "options"))
    return JsonResponse({"questions": questions})


@csrf_exempt
@require_POST
def submit_answers(request):
    try:
        payload = json.loads(request.body or "{}")
    except json.JSONDecodeError:
        return JsonResponse({"error": "Noto'g'ri JSON format."}, status=400)

    answers = payload.get("answers", {})
    question_ids = [int(question_id) for question_id in answers.keys()]
    questions = Question.objects.filter(id__in=question_ids)

    correct_count = 0
    results = []

    for question in questions:
        selected = answers.get(str(question.id))
        is_correct = selected == question.correct_option
        if is_correct:
            correct_count += 1

        results.append(
            {
                "question_id": question.id,
                "selected": selected,
                "correct_option": question.correct_option,
                "is_correct": is_correct,
            }
        )

    total_answered = len(results)
    score_percent = round((correct_count / total_answered) * 100, 1) if total_answered else 0

    return JsonResponse(
        {
            "correct_count": correct_count,
            "total_answered": total_answered,
            "score_percent": score_percent,
            "results": results,
        }
    )
