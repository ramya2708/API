from django.urls import path
from users.api_views import register
from users.api_views import login

urlpatterns=[
    path('user_register', register, name='user_register'),
    path('user_login',login,name='user_login')
]
