import re
from django import forms
from django.utils.text import slugify
from blog.models import Post, Tag, Comment

class PostForm(forms.ModelForm):
	title = forms.CharField()
	body = forms.CharField(widget=forms.Textarea)
	date_time = forms.DateTimeField(input_formats=['%Y-%m-%d %H:%M:%S'], widget=forms.HiddenInput)
	tags = forms.CharField(min_length=1,required=False)
	timestamp = forms.IntegerField(widget=forms.HiddenInput)

	def clean(self):
		cleaned_data = self.cleaned_data
		tags = cleaned_data.get('tags')
		if tags:
			if re.search(r"[^-\w, ]",tags):
				self.add_error('tags', 'Invalid character(s) in tags, only alphanumeric chars and - allowed')
		return cleaned_data

	class Meta:
		model = Post
		fields = ['title', 'body','date_time','timestamp']


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

class SearchForm(forms.Form):
	search= forms.CharField(label="Search...", max_length=256)