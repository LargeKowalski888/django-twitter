from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import Profile, Meep

#Removes groups in admin panel
admin.site.unregister(Group)

#Mix profile info with User info
class ProfileInline(admin.StackedInline):
	model = Profile

#Extends User Model
class UserAdmin(admin.ModelAdmin):
	model = User
	#Just display username fields on admin page
	fields = ["username"]
	inlines = [ProfileInline]

#Unregister initial user
admin.site.unregister(User)
#Reregister User and profile
admin.site.register(User, UserAdmin)
#admin.site.register(Profile)

#Registers the meeps
admin.site.register(Meep)
