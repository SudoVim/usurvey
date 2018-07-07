from django import forms
from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView

from .models import SurveyQuestion, SurveyResponse

class SurveyResponseForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.question = None
        if not self.instance.pk:
            self.question = self.initial['question']

        else:
            self.question = self.instance.question

        self.fields['answer'].label = ''
        self.fields['answer'].choices = \
            self.question.answers.values_list('pk', 'answer')

    class Meta:
        model = SurveyResponse
        fields = ('ip', 'question', 'answer')
        widgets = {
            'ip': forms.HiddenInput(),
            'question': forms.HiddenInput(),
            'answer': forms.RadioSelect(),
        }

class SurveyResponseViewMixin(object):
    """
        mixin object that applies to both create and update views
    """
    model = SurveyResponse
    form_class = SurveyResponseForm
    template_name = 'survey/surveyresponse.html'

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        if 'question' not in kwargs:
            kwargs['question'] = kwargs['form'].question

        return kwargs

    def get_success_url(self):
        return '/'

class SurveyResponseCreateView(SurveyResponseViewMixin, CreateView):
    pass
class SurveyResponseUpdateView(SurveyResponseViewMixin, UpdateView):

    def get_object(self, *args, **kwargs):
        return self.object

def survey_response(request):
    """
        guest is requesting a survey question to answer
    """
    if request.method == 'GET':
        # Randomly generate the question.
        question = SurveyQuestion.random()
        ip = request.META['REMOTE_ADDR']

    else:
        question = SurveyQuestion.objects.get(pk=int(request.POST['question']))
        ip = request.POST['ip']

    # Check to see if an instance already exists
    try:
        instance = SurveyResponse.objects.get(
            question=question,
            ip=ip,
        )

    except SurveyResponse.DoesNotExist:
        instance = None

    view = None
    if instance is None:
        view = SurveyResponseCreateView()
        view.initial = {'question': question, 'ip': ip}

    else:
        view = SurveyResponseUpdateView()
        view.object = instance

    view.request = request
    view.args = tuple()
    view.kwargs = {}
    return view.dispatch(request)
