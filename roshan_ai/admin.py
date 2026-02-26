from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import RoshanTag, RoshanDocument, RoshanQuestion

@admin.register(RoshanTag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name",)

@admin.register(RoshanDocument)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "short_summary", "tag", "created_at")
    list_display_links = ['title']
    search_fields = ("title", "content", "summary")
    list_filter = ("tag",)
    ordering = ("-created_at",)

    def short_summary(self, obj):
        return obj.summary[:50] + "..." if len(obj.summary) > 50 else obj.summary
    
    short_summary.short_description = "Summary"

@admin.register(RoshanQuestion)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("id", "short_question", "related_document", "created_at")
    list_display_links = ['short_question']
    search_fields = ("question_text", "answer")
    ordering = ("-created_at",)

    def short_question(self, obj):
        return obj.question_text[:50] + "..." if len(obj.question_text) > 50 else obj.question_text
    
    def related_document(self, obj):
        if obj.document:
            url = reverse(
                'admin:roshan_ai_roshandocument_change',
                args=[obj.document.id]
            )
            return format_html(
                '<a href="{}">{}</a>',
                url,
                obj.document.title
            )
        return "-"
    
    short_question.short_description = "Question"
    related_document.short_description = "Related Document"
