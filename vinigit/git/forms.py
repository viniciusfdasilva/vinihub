from django import forms
from django.contrib.auth.models import User
from git.models import PullRequest, Release
from django.forms.models import ModelForm

class UserForm(ModelForm):
    
    class Meta:
        model = User
        fields = ['username', 'password']
        

class PullRequestForm(ModelForm):
    
    class Meta:
        model  = PullRequest
        fields = ['title', 'description']
        
class ReleaseForm(ModelForm):
    
    class Meta:
        model = Release
        fiealds = ['release_name', 'description', 'changelog']