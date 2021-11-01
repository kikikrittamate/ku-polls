"""Create admin page."""

from django.contrib import admin

from .models import Choice, Question, Vote


class ChoiceInline(admin.TabularInline):
    """Admin can add the choice in question in default 3 fields."""

    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    """Admin can custom the question in admin page."""

    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date', 'end_date'],
                              'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date', 'was_published_recently',
                    'is_published', 'can_vote')
    list_filter = ['pub_date']
    search_fields = ['question_text']


admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Vote)
