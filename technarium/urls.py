"""technarium URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url, include
from django.contrib import admin
from blog import views

urlpatterns = [
    url(r'^$', views.post_list),
    url(r'^page/(?P<page_num>[\w\d+]+)/$', views.post_list, name='page'),
    url(r'^admin/', admin.site.urls),
    url(r'^tagged/(?P<tag_name>[-\w\d]+)/$', views.tagged_post_list,name='view_tagged_posts'),
    url(r'^tagged/(?P<tag_name>[-\w\d]+)/page/(?P<page_num>[\w\d]+)/$', views.tagged_post_list, name='view_tagged_posts'),
    url(r'^author/(?P<username>[-\w\d]+)/page/(?P<page_num>[\w\d]+)/$', views.posts_by_author, name='view_posts_by_author'),
    url(r'^author/(?P<username>[-\w\d]+)/$', views.posts_by_author, name='view_posts_by_author'),
    url(r'^edit_post/(?P<pk>[\w\-]+)/(?P<slug>[\w\d-]+)?$', views.edit_post, name='edit_post'),
    url(r'^add_post/$', views.add_post, name='add_post'),
    url(r'^delete_post/(?P<pk>[\d+]+)/(?P<slug>[\w\d-]+)?$', views.delete_post, name='delete_post'),
    url(r'^delete_comment/(?P<pk>[\d+]+)/$', views.delete_comment, name='delete_comment'),
    url(r'^comment/(?P<pk>[\w+\d+]+)/(?P<slug>[\w\d-]+)?$', views.add_comment, name='add_comment'),
    url(r'^post/(?P<pk>[\w\d]+)/(?P<slug>[\w\d-]+)?$', views.single_post_view, name='single_post_view'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)