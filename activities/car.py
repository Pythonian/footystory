from __future__ import unicode_literals

from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings

User = settings.AUTH_USER_MODEL

# To specify a default user to replace when a user
# has been deleted.

# def get_sentinel_user():
#     return get_user_model().objects.get_or_create(username='deleted')[0]

# class MyModel(models.Model):
#     user = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.SET(get_sentinel_user),
#     )

def set_delete_user():
	User = get_user_model()
	return User.objects.get_or_create(
		username='deleted')[0] # get_or_create returns a tuple obj
	# You can create a qs not to allow cars with a delete user to show

def limit_car_choices():
	Q = models.Q
	return Q(username__icontains='e')
	#return {'is_staff': True}

class Car(models.Model):
	name = models.CharField(max_length=100)
	#user = models.ForeignKey(User)
	# driver = models.ManyToManyField(User,
	# 	on_delete=models.SET_NULL,
	# 	default=1)
	user = models.ForeignKey(User,
		on_delete=models.SET_DEFAULT,
		default=1,
		limit_choices_to=limit_car_choices)
	updated_by = models.ForeignKey(
		User,
		related_name='updated_car_user',
		null=True,blank=True)
	#passengers = models.ManyToManyField(User)


	def __unicode__(self):
		return self.name


############
## Admin ###
############

from django.contrib import admin

from .models import Car

class CarAdmin(admin.ModelAdmin):
	search_fields = ['user__username', 'user__email']
	raw_id_fields = ['user']
	readonly_fields = ['updated_by']

	def save_model(self, request, obj, form, change):
		if change:
			obj.updated_by = request.user
		obj.save()

	# To get a queryset based on the logged in user
	# def get_queryset(self, request):
	# 	qs = super(CarAdmin, self).get_queryset(request)
	# 	if request.user.is_superuser:
	# 		return qs
	# 	return qs.filter(user=request.user)

	# # The user who created the object only
	# # has the ability to delete or edit it
	# def has_change_permission(self, request, obj=None):
	# 	"""the user must be a staff"""
	# 	if not obj:
	# 		return True
	# 	return obj.user == request.user or request.user.is_superuser

	# def get_readonly_fields(self, request, *args, **kwargs):
	# 	if request.user.is_superuser:
	# 		return []
	# 	return ['user']

admin.site.register(Car, CarAdmin)

