from django import forms
from django.contrib.auth.models import User
from git.models import PullRequest
from django.forms.models import ModelForm

class UserForm(ModelForm):
    
    class Meta:
        model = User
        fields = ['username', 'password']
        

class PullRequestForm(ModeForm):
    
    class Meta:
        model  = PullRequest
        fields = ['title', 'description']