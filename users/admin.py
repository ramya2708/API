from django.contrib import admin
from users.models import LoginUser
# Register your models here.

class LoginUserAdmin(admin.ModelAdmin):
    search_fields = ['pk']
    list_filter = ['user_id']
    list_display = [
        'pk',
        'user_id',
        'otp',
        # 'fcm_token',
        'country',
        # 'fb_link',
        # 'insta_link',
        # 'twitter_link',
        'is_deleted',
        'created_at',
        'updated_at',
    ]
    list_editable = ['user_id']
admin.site.register(LoginUser, LoginUserAdmin)