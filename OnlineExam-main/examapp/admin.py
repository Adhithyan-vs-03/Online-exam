from django.contrib import admin

# Register your models here.


# admin.py
from django.contrib import admin
from .models import Exam, Question, Option, StudentProfile, UserAnswer

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ['title', 'duration', 'created_at']
    search_fields = ['title', 'description']

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['text', 'exam', 'subject']
    list_filter = ['exam', 'subject']
    search_fields = ['text']

@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ['text', 'question', 'is_correct']
    list_filter = ['question__exam', 'is_correct']

admin.site.register(StudentProfile)
admin.site.register(UserAnswer)