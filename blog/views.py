import re
import time
import urllib.parse
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from blog.models import Post, Tag, Comment, UserProfile
from blog.forms import PostForm, CommentForm, DeletePost
from blog.utils import write_file, get_query


def redirector(request):
	'''redirects old urls to new ones. /join.html/?language=lt >> /join/en/'''

	if 'language' in request.GET:
		lang = request.GET['language']
	else:
		lang = 'en'
	url = request.get_full_path() # >> '/index.html'
	url = re.split(r'\.', url)[0] # >> '/index'
	if url =='/index': # main page doesn't follow /resource/language/ convention so we process it separately
		if lang == 'en': 
			return HttpResponseRedirect('/')
		else:
			return HttpResponseRedirect('/lt')
	else:
		url = url + '/' + lang 	
		return HttpResponseRedirect(url)


@login_required
@csrf_exempt
def upload_handler(request):
	if request.method == 'POST':
		filename = str(request.FILES['file'])
		write_file(filename, request.FILES['file'])
		return HttpResponse('{ "location" :'+ '"/media/usr/'+filename+'"}')

def search(request, query_string=None, page_num=1):
	page_num=int(page_num)
	if query_string == None:
		''' this is for the first page of the result where query is passed trough 
		the request's payload instead of the url''' 
		if ('q' in request.GET) and request.GET['q'].strip():
			query_string = request.GET['q']  			
			entry_query = get_query(query_string, ['title', 'body','tags__name'])     
			found_entries = Post.objects.filter(entry_query).order_by('-date_time').distinct()[page_num*10-10:page_num*10]
			context_dict = {'query_string': query_string, 'post_list': found_entries }
	else:
		query_string = urllib.parse.unquote_plus(query_string)
		entry_query = get_query(query_string, ['title', 'body','tags__name'])     
		found_entries = Post.objects.filter(entry_query).order_by('-date_time').distinct()[page_num*10-10:page_num*10]
		context_dict = {'query_string': query_string, 'post_list': found_entries }


	if page_num == 1: #render full page if we're on the first pageq
		return render(request, 'blog/post_list.html', context_dict)
	else: # else render only the post_list without header, etc
		return render(request, 'blog/post_list_template.html', context_dict) 

def post_list(request, page_num=1):
	page_num=int(page_num)
	post_list = Post.objects.all().order_by('-date_time')[page_num*10-10:page_num*10] # query next 10 posts
	tag_list = Tag.objects.all()
	context_dict={'post_list': post_list, 'page_num': page_num}
	if page_num == 1: #render full page if we're on the first page
		return render(request, 'blog/post_list.html', context_dict)
	else: # else render only the post_list without header, etc
		return render(request, 'blog/post_list_template.html', context_dict) 

def single_post_view(request, pk, slug=None): 
	# slug is only for eye candy in the url, we get posts by primary key (pk)
	post = Post.objects.get(pk=pk)
	context_dict={'post':post}
	return render(request, 'blog/single_post_view.html', context_dict)

def tagged_post_list(request, tag_name, page_num=1):
	page_num=int(page_num)
	tag = Tag.objects.get(name=tag_name)
	tagged_post_list = tag.post_set.all().order_by('-date_time')[page_num*10-10:page_num*10] # query next 10 tagged posts
	context_dict = {'post_list':tagged_post_list, 'page_num': page_num, 'current_tag':tag_name}
	if page_num == 1: #render full page if we're on the first page
		return render(request, 'blog/post_list.html', context_dict)
	else: # else render only the post_list without header, etc
		return render(request, 'blog/post_list_template.html', context_dict)

def posts_by_author(request, username, page_num=1):
	page_num = int(page_num)
	user = User.objects.get(username = username)
	user = UserProfile.objects.get(user = user)
	post_list = user.post_set.all().order_by('-date_time')[page_num*10-10:page_num*10] # query next 10 tagged posts
	context_dict = {'post_list': post_list, 'page_num':page_num}
	if page_num == 1: #render full page if we're on the first page
		return render(request, 'blog/post_list.html', context_dict)
	else: # else render only the post_list without header, etc
		return render(request, 'blog/post_list_template.html', context_dict)

@login_required(login_url="/login/")
def edit_post(request, pk,slug=None):
	post = Post.objects.get(pk=pk)
	user = UserProfile.objects.get(user=request.user)


	if not request.user.is_superuser: # if not admin and not post creator return 403
		if user != post.created_by:
			return HttpResponseForbidden()

	if request.method == 'POST':
		form = PostForm(request.POST, instance=post) #overwrite the db entry for the Post instance
		if form.is_valid():
			# tags are processed separately, the field for the post instance is cleared and the new tags are added to it.

			post.tags.all().delete()
			tag_list = form.cleaned_data['tags'].split(',')
			tag_list = [tag.rstrip() for tag in tag_list if tag != ' ' and tag != ''] # clean 
			#tag_list = map(lambda tag: re.sub(r' ', r'-', tag.lower()), tag_list) #clean
			for tag in tag_list:
				tag, created=Tag.objects.get_or_create(name=slugify(tag)) 
				post.tags.add(tag)
						
			form.save()
			return HttpResponseRedirect(reverse('single_post_view', kwargs={'pk':pk, 'slug':slug}))
		else:
			return render(request, 'blog/edit_post.html', {'form':form})

	else:
		# unbound form - send all the tags to be prefilled as a str to the tags field in the form - 'tag, tag2,'
		tags=str(post.tags.all())
		tags=re.findall(r'[-_\w+]+', tags)
		tags=[tag+',' for tag in tags if tag != 'Tag'] # can't remember why !='Tag'
		tags = ' '.join(tags)
		form=PostForm(initial={'body':post.body.encode('UTF-8'), 
								'title':post.title,
								'date_time':post.date_time,
								'tags':tags,
								'timestamp':int(time.time()),
								})

		return render(request, 'blog/edit_post.html', {'form':form})

@login_required(login_url="/login/")
def delete_post(request, pk,slug=None):
	
	post=get_object_or_404(Post, pk=pk)
	

	user = UserProfile.objects.get(user=request.user)
	if not request.user.is_superuser: # if not admin and not post creator return 403
		if user != post.created_by:
			return HttpResponseForbidden()

	if request.method == "POST":
		form = DeletePost(request.POST, instance=post)
		if form.is_valid():
			post.delete()
			return HttpResponseRedirect('/blog/')
	else:
		form = DeletePost(instance=post)
		return render(request,'blog/delete_object.html', {'form':form, 'post':post})

@user_passes_test(lambda u: u.is_superuser)
def delete_comment(request, pk):
	if not request.user.is_superuser: #only admin can delete comments for now
		return HttpResponseForbidden()

	comment=get_object_or_404(Comment, pk=pk)
	if request.method == "POST":
		form = DeletePost(request.POST, instance=comment)
		if form.is_valid():
			comment.delete()
			return HttpResponseRedirect(reverse('single_post_view', kwargs={'pk':comment.post.pk}))
	else:
		form = DeletePost(instance=comment)
		return render(request,'blog/delete_object.html', {'form':form, 'comment':comment})

@login_required(login_url="/login/")
def add_post(request):
	
	if request.method == 'POST':
		form = PostForm(request.POST)
		user = UserProfile.objects.get(user=request.user)
		if form.is_valid():
			tag_list = form.cleaned_data['tags'].split(',')
			tag_list = [tag.rstrip() for tag in tag_list if tag != ' ' and tag != ''] # clean 

			obj = form.save()
			obj.slug=slugify(request.POST['title'])
			obj.created_by = user
			for tag in tag_list:
				tag, created=Tag.objects.get_or_create(name=slugify(tag))
				obj.tags.add(tag)
			obj.save()
			return HttpResponseRedirect(reverse('single_post_view', kwargs={'pk':obj.pk, 'slug':obj.slug}))
	else:
		form = PostForm(initial={'timestamp':int(time.time()),
								'date_time': time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())})

	return render(request, 'blog/add_post.html', {'form':form})

def add_comment(request, pk, slug=None):
	post = Post.objects.get(pk=pk)
	if request.method == 'POST':
		form = CommentForm(request.POST)
		if form.is_valid():
			obj=form.save(commit=False)
			obj.post_id=pk
			form.save()
			return HttpResponseRedirect(reverse('single_post_view', kwargs={'pk':pk}))
	else:
		form = CommentForm(initial={'date_time': time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())})
	return render(request, 'blog/add_comment.html', {'form':form, 'post':post})

def user_login(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(username=username, password=password)

		if user:
			if user.is_active:
				login(request, user)
				return redirect('/')
			else:
				return HttpResponse('Account is disabled')
		else:
			return HttpResponse('Username or password is incorrect')
	else:
		return render(request, 'blog/login.html', {})

@login_required(login_url="/login/")
def user_logout(request):
	logout(request)
	return redirect('/')