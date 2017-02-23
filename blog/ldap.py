from django.conf import settings
from django.contrib.auth.models import User
from blog.models import UserProfile
from ldap3 import Server, Connection


def connect(username, password):
	'''authenticate to technarium ldap server, 
	return True if username or password combination 
	is correct and user belongs to group "Members"'''


	server = Server('ldaps://ldap.technarium.lt')
	dn = 'uid=blog,ou=Services,dc=technarium,dc=lt'
	pw = '' # secret here
	try:
		conn = Connection(server,dn,pw,auto_bind=True)
		conn.search('ou=Members,dc=technarium,dc=lt','(uid='+username+')',attributes='cn')
	except:
		# service bind failed.
		return False
	if not conn.entries: 
		# username not found
		return False

	else:
		udn = 'cn='+str(conn.entries[0].cn)+',ou=Members,dc=technarium,dc=lt' # create the user's dn 
		conn.search('ou=Groups,dc=technarium,dc=lt','(cn=members)', attributes='uniqueMember') # search for the Members group
		member_list = conn.entries[0].uniqueMember # get a list of users in group Members
		udn = udn.encode('utf-8').decode('unicode_escape') # urgh
		if udn not in member_list:
			#user is not in "Members" group 
			return False
		try:
			new_conn=Connection(server,udn,password,auto_bind=True)
			# success
			return True
		except:
			#  LDAPBindError - password is incorrect, or if something else happens.
			return False



class LdapLogin:

	def authenticate(self, username=None,password=None):

		if not connect(username, password):
			# authentication failed
			return None
		else:
			user, created = User.objects.get_or_create(username = username)
			UserProfile.objects.get_or_create(user = user)

			return user

	def get_user(self, user_id):
		try:
			return User.objects.get(pk=user_id)
		except User.DoesNotExist:
			return None
