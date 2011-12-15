from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from basegd.models import UserProfile

class UserProfileInline(admin.TabularInline):
    model = UserProfile
    fk_name = 'user'
    max_num = 1
   
class CustomUserAdmin(UserAdmin):
    inlines = [UserProfileInline,]
       
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
