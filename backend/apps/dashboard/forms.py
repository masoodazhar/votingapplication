from django import forms
from django.forms import inlineformset_factory
from .models import Vote, Answer, VoteChoice

class VoteForm(forms.ModelForm):
    class Meta:
        model = Vote
        fields = ['question', 'expired_at']
        widgets = {
            'expired_at': forms.TextInput(attrs={'type': 'datetime-local'}),
        }

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text']

VoteChoiceFormSet = inlineformset_factory(
    Vote, 
    VoteChoice,
    fields=['text'],
    widgets={'text': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Choices'})},
    extra=3
)