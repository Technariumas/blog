import re
import time
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from blog.models import Post, Tag, Comment
from blog.forms import PostForm, CommentForm, DeletePost

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

def tagged_post_list(request, tag_pk, page_num=1):
	page_num=int(page_num)
	tag = Tag.objects.get(pk=tag_pk)
	tagged_post_list = tag.post_set.all().order_by('-date_time')[page_num*10-10:page_num*10] # query next 10 tagged posts
	tag_list = Tag.objects.all()
	context_dict = {'post_list':tagged_post_list, 'page_num': page_num, 'current_tag':tag_pk}
	if page_num == 1: #render full page if we're on the first page
		return render(request, 'blog/post_list.html', context_dict)
	else: # else render only the post_list without header, etc
		return render(request, 'blog/post_list_template.html', context_dict) 

@login_required(login_url="/login/")
def edit_post(request, pk):
	post = Post.objects.get(pk=pk)
	if request.method == 'POST':
		form = PostForm(request.POST, instance=post) #overwrite the db entry for the Post instance
		if form.is_valid():
			# tags are processed separately, the field for the post instance is cleared and the tags are added to it.
			post.tags.all().delete()
			tag_list = form.cleaned_data['tags'].split('#')
			tag_list = [tag.rstrip() for tag in tag_list if tag != ' ' and tag != ''] # clean 
			tag_list = map(lambda tag: re.sub(r' ', r'-', tag.lower()), tag_list) #clean
			for tag in tag_list:
				tag, created=Tag.objects.get_or_create(name=slugify(tag)) 
				post.tags.add(tag)
			form.save()
			return HttpResponseRedirect(reverse('single_post_view', kwargs={'pk':pk}))

	else:
		# unbound form - send all the tags to be prefilled as a str to the tags field in the form - '#tag #tag2'
		tags=str(post.tags.all())
		tags=re.findall(r'[-_\w+]+', tags)
		tags=['#'+tag for tag in tags if tag != 'Tag']
		tags = ' '.join(tags)
		form=PostForm(initial={'body':post.body.encode('UTF-8'), 
								'title':post.title,
								'date_time':post.date_time,
								'tags':tags,
								'timestamp':int(time.time()),
								})

		return render(request, 'blog/edit_post.html', {'form':form})

@login_required(login_url="/login/")
def delete_post(request, pk):
	post=get_object_or_404(Post, pk=pk)
	if request.method == "POST":
		form = DeletePost(request.POST, instance=post)
		if form.is_valid():
			post.delete()
			return HttpResponseRedirect('/')
	else:
		form = DeletePost(instance=post)
		return render(request,'blog/delete_object.html', {'form':form, 'post':post})

@login_required(login_url="/login/")
def delete_comment(request, pk):
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
		if form.is_valid():
			tag_list = form.cleaned_data['tags'].split('#')
			tag_list = [tag.rstrip() for tag in tag_list if tag != ' ' and tag != ''] # clean 
			tag_list = map(lambda tag: re.sub(r' ', r'-', tag.lower()), tag_list)

			obj = form.save()
			obj.slug=slugify(request.POST['title'])
			for tag in tag_list:
				tag, created=Tag.objects.get_or_create(name=slugify(tag))
				obj.tags.add(tag)
			return HttpResponseRedirect(reverse('single_post_view', kwargs={'pk':obj.pk}))
	else:
		form = PostForm(initial={'timestamp':int(time.time()),
								'date_time': time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())})
	return render(request, 'blog/add_post.html', {'form':form})

def add_comment(request, pk):
	post = Post.objects.get(pk=pk)
	if request.method == 'POST':
		form = CommentForm(request.POST)
		if form.is_valid():
			obj=form.save(commit=False)
			obj.post_id=pk
			form.save()
			return HttpResponseRedirect(reverse('single_post_view', kwargs={'pk':pk}))
		else:
			print('inv`')
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