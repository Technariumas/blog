from django.contrib import admin
from blog.models import Post, Tag, Comment, UserProfile
# Register your models here.

admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(Comment)
admin.site.register(UserProfile)