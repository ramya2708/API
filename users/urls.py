from django.urls import path
#from users.api_views import register
from users.api_views import register,login,verify_otp,verify_otplogin,profile_image_upload,resend_otp,profile_update,user_detail

urlpatterns=[
    path('user_register', register, name='user_register'),
    path('user_login', login, name='user_login'),
    path('verify_otp', verify_otp, name='verify_otp'),
    path('verify_otplogin', verify_otplogin, name='verify_otplogin'),
    path('profile_image_upload', profile_image_upload, name='profile_image_upload'),
    path('resend_otp', resend_otp, name='resend_otp'),
    path('profile_update', profile_update, name='profile_update'),
    path('user_detail/<int:mobile_no>', user_detail, name='user_detail'),
]
