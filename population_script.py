'''Population script to get posts from blog.technarium.com to database, only works for post type == text
for now.'''

import requests
import json
import os
import django
from django.template.defaultfilters import slugify
from datetime import datetime

POST_COUNT=400 # how many posts to get.
API_KEY = '' #put tumblr api key here

def main():

	for i in range(0,POST_COUNT,20):
		api_key = '?api_key=' + API_KEY
		base_url = 'https://api.tumblr.com/v2/blog/blog.technariumas.lt/posts'
		limit = '&limit=20'
		offset = '&offset='+str(i)
		uri=base_url+api_key+limit+offset
		response = requests.get(uri)
		post = json.loads(response.text)
		post = post['response']
		for post in post[u'posts']:
			slug = post[u'slug']
			if post[u'type']=='text':
				title = post[u'title']
				date_time = datetime.strptime(post[u'date'], '%Y-%m-%d %H:%M:%S %Z')
				body = post[u'body']
				timestamp = post[u'timestamp']
				tags = post[u'tags']
				post_obj=add_post(title,slug,date_time,timestamp,body)
				for tag in tags:
					tag_obj =add_tag(tag.lower())
					post_obj.tags.add(tag_obj)


def add_tag(name):
	obj, created = Tag.objects.get_or_create(name=slugify(name))
	return obj

def add_post(title, slug, date_time, timestamp, body):
	obj, created = Post.objects.get_or_create(title=title, slug=slug,date_time=date_time,body=body,timestamp=timestamp)
	return obj
	
if __name__ == '__main__':
	os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'technarium.settings')
	django.setup()
	from blog.models import Post, Tag
	main()