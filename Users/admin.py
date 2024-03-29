# # Users/admin.py
# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
# from .models import CustomUser


# class CustomUserAdmin(UserAdmin):
#     model = CustomUser
#     list_display = ('email', 'first_name', 'last_name',
#                     'is_active', 'is_staff')
#     search_fields = ('email', 'first_name', 'last_name')
#     ordering = ('email',)


# admin.site.register(CustomUser, CustomUserAdmin)


# Users/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UserDetails

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'first_name', 'last_name',
                    'is_active', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    # ordering = ('email',)
    ordering = ('username',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('username', 'first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active',
         'is_staff', 'groups', 'user_permissions')}),
    )


admin.site.register(CustomUser, CustomUserAdmin)
