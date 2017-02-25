from bs4 import BeautifulSoup
from django.conf import settings
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def write_file(filename, f):
    with open('media/usr/'+filename, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def delete_images(old_post_body, post_body=None, delete=False):
	'''utility to clean up unused images. To be called whenever the post body is changed or the whole post is deleted.'''
	if delete:
		old_soup = BeautifulSoup(old_post_body, 'html.parser')
		old_imgs = [img.get('src') for img in old_soup.find_all('img')]
		for img in old_imgs:
			try:
				os.remove(BASE_DIR+img)
				print('removed:  ',img)
			except FileNotFoundError:
				print('unable to delete '+img+'. File not found')
	else:
		old_soup = BeautifulSoup(old_post_body, 'html.parser')
		new_soup = BeautifulSoup(post_body, 'html.parser')
		old_imgs = [img.get('src') for img in old_soup.find_all('img')]
		new_imgs = [img.get('src') for img in new_soup.find_all('img')]
		for img in old_imgs:
			if img not in new_imgs:
				try:
					os.remove(BASE_DIR+img)
					print('removed:  ',img)
				except FileNotFoundError:
					print('unable to delete '+img+'. File not found')