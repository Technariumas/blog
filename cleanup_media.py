import os
import django 
from bs4 import BeautifulSoup
BASE_DIR = os.path.dirname(os.path.abspath(__file__))



def get_used_images():
	images=[]
	all_posts = Post.objects.all()
	all_posts = [post.body for post in all_posts]
	for post in all_posts:
		soup = BeautifulSoup(post, 'html.parser')
		imgs = [os.path.normpath(BASE_DIR+img.get('src')) for img in soup.find_all('img') if img.get('src').startswith('/media')]
		images += imgs
	return images

def get_all_images():
	images = os.listdir(os.path.join(BASE_DIR, 'media', 'usr'))
	images = [os.path.join(BASE_DIR,'media','usr',img) for img in images]
	return images

def main():
	counter = 0
	for file in get_all_images():
		if file not in get_used_images():
			os.remove(file)
			counter +=1
			print('removed',file)
	print('Removed '+ str(counter) + ' files')




if __name__ == '__main__':
	os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'technarium.settings')
	django.setup()
	from blog.models import Post
	main()