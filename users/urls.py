from django.urls import path
from users.api_views import register

urlpatterns=[
    path('user_register', register, name='user_register'),
]
