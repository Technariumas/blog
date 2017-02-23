from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

class Tag(models.Model):
	name = models.CharField(max_length=128, unique=True)

	def __str__(self):
		return self.name

class Comment(models.Model):
	posted_by = models.CharField(max_length=128, null=True)
	body = models.TextField()
	date_time = models.DateTimeField()
	post = models.ForeignKey('Post')

	def __str__(self):
		return self.body

class Post(models.Model):
	title = models.CharField(max_length=128, default='No title', null=True, blank=True)
	body = models.TextField()
	slug = models.SlugField()
	date_time = models.DateTimeField()
	timestamp = models.IntegerField()
	tags = models.ManyToManyField(Tag,null=True,blank=True)
	created_by = models.ForeignKey('UserProfile', null=True)

	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = slugify(self.title)
		super(Post, self).save(*args, **kwargs)

	class Meta:
		ordering = ['-date_time']

	def __str__(self):
		return self.slug

class UserProfile(models.Model):
	user = models.OneToOneField(User) # required

	def __str__(self):
		return self.user.username