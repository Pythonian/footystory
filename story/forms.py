from django import forms
from .models import Story, Comment


class StoryForm(forms.ModelForm):
	tags = forms.CharField(
		label='Add Tags',
		widget=forms.TextInput(attrs={'class': 'form-control'}),
		max_length=255, 
		required=False,
		help_text='Use spaces to separate the tags.')
	
	class Meta:
		model = Story
		fields = ['title', 'image', 'body', 'topic', 'status', 'tags']


class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ['body']
