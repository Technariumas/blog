import re
from django import forms
from django.utils.text import slugify
from blog.models import Post, Tag, Comment

class PostForm(forms.ModelForm):
	title = forms.CharField()
	body = forms.CharField(widget=forms.Textarea)
	date_time = forms.DateTimeField(input_formats=['%Y-%m-%d %H:%M:%S'], widget=forms.HiddenInput)
	tags = forms.CharField(min_length=1,)
	timestamp = forms.IntegerField(widget=forms.HiddenInput)

	def clean(self):
		cleaned_data = self.cleaned_data
		tags = cleaned_data.get('tags')
		if re.search(r"[^-\w$-_.+!*'(), ]",tags):
			self.add_error('tags', 'Invalid character(s) in tags')
		return cleaned_data

	class Meta:
		model = Post
		fields = ['title', 'body','date_time','timestamp']



	
'''
	def clean_tags(self):
		data=self.cleaned_data['tags']
		if re.search(r'[^-\w# ]',data):
			self.add_error('tags', 'Invalid character(s) in tags')
		return data
'''




class CommentForm(forms.ModelForm):
	posted_by = forms.CharField()
	body = forms.CharField(widget=forms.Textarea)
	date_time = forms.DateTimeField(widget=forms.HiddenInput)

	class Meta:
		model = Comment
		fields = ['body', 'date_time', 'posted_by']

class DeletePost(forms.ModelForm):
	class Meta:
		model = Post
		fields = []

class DeleteComment(forms.ModelForm):
	class Meta:
		model = Comment
		fields = []