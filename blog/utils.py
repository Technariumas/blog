from bs4 import BeautifulSoup
from django.conf import settings

def write_file(filename, f):
    with open('media/usr/'+filename, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
