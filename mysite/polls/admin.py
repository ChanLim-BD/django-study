from tkinter.messagebox import QUESTION
from django.contrib import admin
from .models import Question, Choice

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['pk']


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ['pk']
    