from django.contrib import admin
from . models import CustomUser
# Register your models here.

class CustomUserAdmin(admin.ModelAdmin):
    search_fields = ['pk']
    list_filter = ['mobile_no', 'email', 'user_role']
    list_display = [
        'pk',
        'username',
        'first_name',  # full name
        'email',
        'user_role',
        'user_profile',
        'mobile_no',
        'is_verified',
        'updated_on',
    ]
    list_editable = ['mobile_no', 'email', 'user_role']
admin.site.register(CustomUser, CustomUserAdmin)