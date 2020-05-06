from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User 

from .models import Profile, Follow


class ProfileInline(admin.StackedInline):
	model = Profile
	can_delete = False
	verbose_name_plural = 'Profile'
	fk_name = 'user'


class CustomUserAdmin(UserAdmin):
	inlines = [ProfileInline]
	list_display = ['username', 'email', 'is_staff', 'get_favorite_club', 'is_active']
	# For optimization, get the Profile relationship of the User model
	list_select_related = ['profile']

	def get_favorite_club(self, obj):
		return obj.profile.favorite_club 
	get_favorite_club.short_description = 'Favorite Club'

	# Display the inlines only in the edit form of the UserAdmin
	def get_inline_instances(self, request, obj=None):
		if not obj:
			return list()
		return super(CustomUserAdmin, self).get_inline_instances(request, obj)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)		
admin.site.register(Follow)
# admin.site.site_header = 'Footystory Admin'