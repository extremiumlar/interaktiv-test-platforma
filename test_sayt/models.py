from django.db import models
from django.core.exceptions import ValidationError


class Question(models.Model):
    text = models.CharField(max_length=255)
    options = models.JSONField()
    correct_option = models.CharField(max_length=255)

    def clean(self):
        if not isinstance(self.options, list) or len(self.options) < 2:
            raise ValidationError({"options": "Kamida 2 ta variant kiriting."})
        if self.correct_option not in self.options:
            raise ValidationError(
                {"correct_option": "To'g'ri javob variantlar ro'yxatida bo'lishi kerak."}
            )

    def __str__(self):
        return self.text
