from django.db import models
from django.forms import widgets
from django.contrib import admin
from .models import SurveyQuestion, SurveyAnswer

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

class SurveyQuestionAdmin(admin.ModelAdmin):
    inlines = [
        SurveyAnswerInline,
    ]

admin.site.register(SurveyQuestion, SurveyQuestionAdmin)
