from django.contrib import admin
from django import forms
import re

from .models import Question


class QuestionAdminForm(forms.ModelForm):
    options_text = forms.CharField(
        label="Javob variantlari",
        widget=forms.Textarea(
            attrs={
                "rows": 6,
                "placeholder": "Har bir variantni yangi qatordan kiriting",
            }
        ),
        help_text="Masalan: Variant 1 (Enter) Variant 2 (Enter) Variant 3",
    )

    class Meta:
        model = Question
        fields = ("text", "options_text", "correct_option")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk and isinstance(self.instance.options, list):
            self.fields["options_text"].initial = "\n".join(self.instance.options)

    def clean_options_text(self):
        raw_value = self.cleaned_data.get("options_text", "")
        chunks = re.split(r"[\n,;]+", raw_value)
        options = [line.strip() for line in chunks if line.strip()]
        if len(options) < 2:
            raise forms.ValidationError(
                "Kamida 2 ta variant kiriting. Har birini yangi qatorda yoki vergul bilan ajrating."
            )
        return options

    def clean_correct_option(self):
        correct_option = (self.cleaned_data.get("correct_option") or "").strip()
        options = self.cleaned_data.get("options_text", [])
        if not correct_option:
            return correct_option

        for option in options:
            if option.strip().lower() == correct_option.lower():
                return option
        return correct_option

    def clean(self):
        cleaned_data = super().clean()
        # Model.clean() runs before save(); populate instance now.
        options = cleaned_data.get("options_text")
        if options is not None:
            self.instance.options = options
        correct_option = cleaned_data.get("correct_option")
        if correct_option is not None:
            self.instance.correct_option = correct_option
        return cleaned_data

    def save(self, commit=True):
        self.instance.options = self.cleaned_data["options_text"]
        return super().save(commit=commit)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    form = QuestionAdminForm
    list_display = ("id", "text", "correct_option")
    search_fields = ("text", "correct_option")
