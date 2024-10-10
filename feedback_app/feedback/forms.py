from django import forms
from .models import Response, Answer, Question

class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['name', 'surname', 'school']

    # Dynamically add fields for each question
    def __init__(self, *args, **kwargs):
        super(ResponseForm, self).__init__(*args, **kwargs)
        questions = Question.objects.all()
        for question in questions:
            self.fields[f'question_{question.id}'] = forms.CharField(label=question.question_text)

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text']
