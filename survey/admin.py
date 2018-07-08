from django.db import models
from django.forms import widgets
from django.contrib import admin
from .models import SurveyQuestion, SurveyAnswer, SurveyResponse

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

def delete_results(modeladmin, request, queryset):
    """
        Delete all results for the given survey questions.
    """
    SurveyResponse.objects.filter(question__in=queryset).delete()
delete_results.short_description = "Delete results"

@admin.register(SurveyQuestion)
class SurveyQuestionAdmin(admin.ModelAdmin):
    inlines = [
        SurveyAnswerInline,
    ]
    actions = [delete_results]
    change_form_template = 'admin/surveyquestion_change_form.html'

    def changeform_view(self, request, *args, **kwargs):
        response = super().changeform_view(request, *args, **kwargs)

        if hasattr(response, 'context_data'):
            question = response.context_data['original']

            if question is not None:
                total_responses = question.responses.count()
                response.context_data['total_responses'] = total_responses
                response.context_data['summary'] = question.answers.\
                    values('answer').\
                    annotate(
                        num_responses=models.Count('responses'),
                    ).\
                    order_by('-num_responses')

        return response
