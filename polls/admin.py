from django.contrib import admin

from .models import Question, Choice


class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["question_text"]}),
        ("Date information", {"fields": ["pub_date"], "classes": ["collapse"]}),
    ]
    inlines = [ChoiceInline]
    list_display = ["question_text", "pub_date", "was_published_recently"]


admin.site.register(Question, QuestionAdmin)


class ChoiceAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["question", "choice_text"]}),
        ("Date information", {"fields": ["votes"]}),
    ]
    list_display = ["question", "choice_text", "votes"]


admin.site.register(Choice, ChoiceAdmin)
