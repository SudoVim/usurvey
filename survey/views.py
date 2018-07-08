from django import forms
from django.shortcuts import render
from django.template.response import SimpleTemplateResponse
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

class SurveyResponseView(CreateView):
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

def survey_response(request):
    """
        guest is requesting a survey question to answer
    """
    view = SurveyResponseView()
    if request.method == 'GET':
        # Get the user's IP address from the metadata.
        ip = request.META['REMOTE_ADDR']

        # Randomly generate the question.
        question = SurveyQuestion.random_for_ip(ip)
        if question is None:
            return SimpleTemplateResponse(
                'survey/surveyresponse_error.html',
                {'error': 'There are no more questions to answer for now.'},
            )

    # The user is submitting an answer, query the ip/question from the POST
    # data.
    else:
        ip = request.POST['ip']
        question = SurveyQuestion.objects.get(pk=int(request.POST['question']))

    # We need to get some initial values here. I don't like it, but that's what
    # the "as_view" method does for class-based views.
    view.initial = {'question': question, 'ip': ip}
    view.request = request
    view.args = tuple()
    view.kwargs = {}
    return view.dispatch(request)
