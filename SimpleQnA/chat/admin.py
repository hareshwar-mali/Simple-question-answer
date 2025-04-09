from django.contrib import admin
from .models import Question, Answer


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'title', 'body', 'created_at']
    search_fields = ['title', 'body', 'user__username']
    list_filter = ['created_at']


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['id', 'question', 'user', 'body', 'created_at', 'total_likes_display']
    search_fields = ['body', 'user__username', 'question__title']
    list_filter = ['created_at']

    def total_likes_display(self, obj):
        return obj.total_likes()

    total_likes_display.short_description = 'Total Likes'
