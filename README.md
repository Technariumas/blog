# blog
New Technarium blog framework.


Clone the repo.
```
pip install -r requirements.txt
```
```
python manage.py runserver
```
Go to 127.0.0.1:8000

test db includes around 350+ posts from http://blog.technariumas.lt/.

logging in allows to edit, create and delete posts and delete comments.

username: a

pw: summer12

default django admin interface is on 127.0.0.1:8000/admin , allows to add, remove users and more. 

## TODO
* Finish front end.
* ~~WYSIWYG editor configurations, has random stuff now.~~
* ~~Tag editor~~
* ~~LDAP authentication - seems to be working, but needs more testing.~~
* ~~User groups? at the moment anyone with an account has access to delete, create or edit anything.~~
* ~~URL inconsistencies.~~
* Finish and test integration with technarium.lt static pages.
* Redirect old urls.
* ~~Image upload and hosting~~
* ?
