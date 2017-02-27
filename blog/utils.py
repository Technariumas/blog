import re
from bs4 import BeautifulSoup
from django.conf import settings
from django.db.models import Q
from blog.forms import SearchForm

def write_file(filename, f):
    with open('media/usr/'+filename, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def search_context(request):
    search_form = SearchForm()

    return {
        'search_form': search_form,
    }


def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
	'''copypasta from http://julienphalip.com/post/2825034077/adding-search-to-a-django-site-in-a-snap'''
	return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)] 

def get_query(query_string, search_fields):
	'''copypasta from http://julienphalip.com/post/2825034077/adding-search-to-a-django-site-in-a-snap'''

	query = None # Query to search for every search term        
	terms = normalize_query(query_string)
	for term in terms:
		or_query = None # Query to search for a given term in each field
		for field_name in search_fields:
			q = Q(**{"%s__icontains" % field_name: term})
			if or_query is None:
				or_query = q
			else:
				or_query = or_query | q
		if query is None:
			query = or_query
		else:
			query = query & or_query
	return query


