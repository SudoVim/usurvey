from django.db import models
from django.forms import widgets
from django.contrib import admin
from .models import SurveyQuestion, SurveyAnswer, SurveyResult, SurveyResponse

class SurveyAnswerInline(admin.TabularInline):
    model = SurveyAnswer

    # I'm just going to use 4 extra fields as I think that's the normal number
    # of responses to a question. This could change easily, or we could make
    # it customizable by defining the get_extra method.
    extra = 4

    # I don't like the textarea for answers. Even though I'm using a BLOB type,
    # The extra room looks bad.
    formfield_overrides = {
        models.TextField: {'widget': widgets.TextInput},
    }

@admin.register(SurveyQuestion)
class SurveyQuestionAdmin(admin.ModelAdmin):
    inlines = [
        SurveyAnswerInline,
    ]

def delete_results(modeladmin, request, queryset):
    """
        Delete all results for the given survey questions.
    """
    SurveyResponse.objects.filter(question__in=queryset).delete()
delete_results.short_description = "Delete results"

@admin.register(SurveyResult)
class SurveyResultAdmin(admin.ModelAdmin):
    actions = [delete_results]

    def get_actions(self, request):
        actions = super().get_actions(request)
        actions.pop('delete_selected', None)
        return actions
