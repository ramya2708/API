from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

from accounts.models import CustomUser
from users.models import LoginUser
from django.core.mail import send_mail, EmailMessage
from django.conf import settings

import random

@api_view(['POST',])
def register(request):
    if request.method == "POST":
        first_name = request.POST['first_name']
        email = request.POST['email']
        mobile_no = request.POST['mobile_no']
        country = request.POST['country']
        if not CustomUser.objects.filter(username=mobile_no).exists():
            print("1")
            user = CustomUser.objects.create(first_name = first_name,
                                            email = email,
                                            mobile_no = mobile_no,
                                            username = mobile_no,
                                            user_role = 2)
            print("2")                                
            number = random.randint(100000,999999)
            LoginUser.objects.create(user_id=user, otp=number, country=country)
            print("3")
            subject = 'Please Confirm Your Account'
            message = 'Your 6 Digit Verification Pin: {}'.format(number)
            email_from = settings.EMAIL_HOST_USER
            recipient_list = to=[str(email)]
            msg = EmailMessage(subject, message, email_from, recipient_list)
            msg.fail_silently=False
            msg.send()

            print('Email send success!')
            return Response({
                "status": 200,
                "message": "success",
                "data":{ "success_message": "user registered successfully sending otp for verification."}
                })
        else:
            return Response({
                "status": 400,
                "message": "failed",
                "data":{"error_message": "mobile number already exists."}
                })
@api_view(['POST',])
def login(request):
    if request.method == "POST":
        email = request.POST['email']
        try:
            if CustomUser.objects.filter(email=email, user_role=2).exists():
                print('1')
                user = CustomUser.objects.get(email=email)
                print(user)
                login_object = LoginUser.objects.get(user_id=user)
                print(login_object)
                if user:
                    token, created = Token.objects.get_or_create(user=user)

                    number = random.randint(100000,999999)
                    login_object.otp = number
                    login_object.save()
                    subject = 'Please Confirm Your Account'
                    message = 'Your 6 Digit Verification Pin: {}'.format(number)
                    email_from = settings.EMAIL_HOST_USER
                    recipient_list = to=[str(email)]
                    msg = EmailMessage(subject, message, email_from, recipient_list)
                    msg.fail_silently=False
                    msg.send()

                    print('Email send success!')
                    print(msg.send())

                    return Response({
                        "status": 200,
                        "message": "success",
                        "data": {
                            'token': token.key,
                            'first_name': user.first_name,
                            'phone_no': user.mobile_no,
                            'email': user.email,
                            'is_verified': user.is_verified,
                            'user_profile': user.user_profile.url
                        }
                    })
                else:
                    return Response({
                        "status": 400,
                        "message": "failed",
                        "data": {
                            "error_message": "Incorrect password"
                        }
                    })
            else:
                return Response({
                    "status": 400,
                    "message": "failed",
                    "data": {
                        "error_message": "Invalid user"
                    }
                })
        except:
            return Response({
                "status": 404,
                "message": "failed",
                "data": {
                    "error_message": "Invalid user"
                }
            })




