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
from users.serializers import UserProfileSerializer

import random

@api_view(['POST',])
def register(request):
    if request.method == "POST":
        first_name = request.POST['first_name']
        email = request.POST['email']
        mobile_no = request.POST['mobile_no']
        country = request.POST['country']
        if not CustomUser.objects.filter(username=mobile_no).exists():

            if not CustomUser.objects.filter(email=email).exists():
                #print("1")
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
                    "data":{"error_message": "email already exists."}
                    })
        else:
            return Response({
                "status": 400,
                "message": "failed",
                "data":{"error_message": "mobile number already exists."}
                })

# @api_view(['POST',])
# def login(request):
#     if request.method == "POST":
#         # email = request.POST['email']
#         mobile_no = request.POST['mobile_no']
#         try:
#             if CustomUser.objects.filter(username=mobile_no, user_role=2).exists():
#                 print('1')
#                 user = CustomUser.objects.get(email=email)
#                 # print(user)
#                 print('2')
#                 login_object = LoginUser.objects.get(user_id=user)
#                 print(login_object)
#                 print('3')
#                 if user:
#                     print('4')
#                     token, created = Token.objects.get_or_create(user=user)

#                     number = random.randint(100000,999999)
#                     login_object.otp = number
#                     login_object.save()

#                     subject = 'Please Confirm Your Account'
#                     message = 'Your 6 Digit Verification Pin: {}'.format(number)
#                     email_from = settings.EMAIL_HOST_USER
#                     recipient_list = to=[str(email)]
#                     msg = EmailMessage(subject, message, email_from, recipient_list)
#                     msg.fail_silently=False
#                     msg.send()

#                     print('Email send success!')
#                     print(msg.send())

#                     return Response({
#                         "status": 200,
#                         "message": "success",
#                         "data": {
#                             'token': token.key,
#                             'first_name': user.first_name,
#                             'phone_no': user.mobile_no,
#                             'email': user.email,
#                             'is_verified': user.is_verified,
#                             'user_profile': user.user_profile.url
#                         }
#                     })
#                 else:
#                     return Response({
#                         "status": 400,
#                         "message": "failed",
#                         "data": {
#                             "error_message": "Incorrect password"
#                         }
#                     })
#             else:
#                 return Response({
#                     "status": 400,
#                     "message": "failed",
#                     "data": {
#                         "error_message": "Invalid user"
#                     }
#                 })
#         except:
#             return Response({
#                 "status": 404,
#                 "message": "failed",
#                 "data": {
#                     "error_message": "Invalid user"
#                 }
#             })  

#login using email and send otp
@api_view(['POST',])
def login(request):
    if request.method == "POST":
        email = request.POST['email']
        try:
            if CustomUser.objects.filter(email=email, user_role=2).exists():
                print('1')
                user = CustomUser.objects.get(email=email)
                # print(user)
                print('2')
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

#verify otp using email and mobile_no
@api_view(['POST',])
def verify_otp(request):
    if request.method == 'POST':
        mobile_no = request.POST['mobile_no']
        email = request.POST['email']
        otp = request.POST['otp']
        if CustomUser.objects.filter(email=email, user_role=2).exists():
            user = CustomUser.objects.get(username=mobile_no)
            user_object = LoginUser.objects.get(user_id=user)
            if user_object.otp == int(otp):
                user.is_verified = True
                user.save()
                return Response({
                    "status": 200,
                    "message": "success",
                    "data": {
                        "success_message": "otp verify successfully."
                    }
                })
            else:
                return Response({
                    "status": 400,
                    "message": "failed",
                    "data": {
                        "error_message": "otp verification failed."
                    }
                })
        else:
            return Response({
                "status": 404,
                "message": "failed",
                "data": {
                    "error_message": "email id not found."
                }
            })
#verify otp using email
@api_view(['POST',])
def verify_otplogin(request):
    if request.method == 'POST':
        email = request.POST['email']
        #email = request.POST.get('email')
        otp = request.POST['otp']
        #otp = request.POST.get('otp')
        if CustomUser.objects.filter(email=email, user_role=2).exists():
            user = CustomUser.objects.get(email=email)
            user_object = LoginUser.objects.get(user_id=user)
            if user_object.otp == int(otp):
                user.is_verified = True
                user.save()
                return Response({
                    "status": 200,
                    "message": "success",
                    "data": {
                        "success_message": "otp verify successfully."
                    }
                })
            else:
                return Response({
                    "status": 400,
                    "message": "failed",
                    "data": {
                        "error_message": "otp verification failed."
                    }
                })
        else:
            return Response({
                "status": 404,
                "message": "failed",
                "data": {
                    "error_message": "email id not found."
                }
            })

#update user profile image
@api_view(['POST',])
@authentication_classes([TokenAuthentication])
@permission_classes((IsAuthenticated,))
def profile_image_upload(request):
    user = request.user
    if request.method == 'POST':
        profile_image = request.FILES['profile_image']
        try:
            if CustomUser.objects.filter(username=request.user, user_role=2).exists():
                print("1")
                user = CustomUser.objects.get(username=request.user)
                user.user_profile = profile_image
                user.save()
                print("2")
                # if user.save():
                return Response({
                    'status': 200,
                    'message': 'success',
                    'data': {
                        'success_message': 'Profile image upload successfully!'
                    }
                })
                # else:
                #     print("4")
                #     return Response({
                #         'status': 400,
                #         'message': 'failed',
                #         'data': {
                #             'error_message': 'Profile image upload failed!'
                #         }
                #     })
            else:
                return Response({
                    'status': 404,
                    'message': 'failed',
                    'data': {
                        'error_message': 'User not found!'
                    }
                })
        except:
            return Response({
                'status': 404,
                'message': 'failed',
                'data': {
                    'error_message': 'Profile image upload failed!'
                }
            })
#resend otp
@api_view(['POST',])
def resend_otp(request):
    if request.method == 'POST':
        email = request.POST['email']
        if CustomUser.objects.filter(email=email, user_role=2).exists():
            user = CustomUser.objects.get(email=email)
            login_object = LoginUser.objects.get(user_id=user)
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
            print(msg)

            if msg.send() == 1:
                return Response({
                    'status': 200,
                    'message': 'success',
                    'data': {
                        'success_message': 'Resend otp send successfully!'
                    }
                })
            else:
                return Response({
                    'status': 400,
                    'message': 'failed',
                    'data': {
                        'error_message': 'Resend otp send failed!'
                    }
                })
        else:
            return Response({
                'status': 404,
                'message': 'failed',
                'data': {
                    'error_message': 'User not found!'
                }
            })
#updating data
@api_view(['POST',])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated,])
def profile_update(request):
    user = request.user
    if request.method == 'POST':
        first_name = request.POST['first_name']
        fb_link = request.POST['fb_link']
        insta_link = request.POST['insta_link']
        twitter_link = request.POST['twitter_link']
        
        if CustomUser.objects.filter(username=user, user_role=2).exists():
            user_object = CustomUser.objects.get(username=user)
            user_object.first_name = first_name
            user_object.save()

            login_object = LoginUser.objects.get(user_id=user)
            login_object.fb_link = fb_link
            login_object.insta_link = insta_link
            login_object.twitter_link = twitter_link
            login_object.save()

            return Response({
                'status': 200,
                'message': 'success',
                'data': {
                    'success_message': 'Profile update successfully!'
                }
            })
        else:
            return Response({
                'status': 400,
                'message': 'failed',
                'data': {
                    'error_message': 'Profile update failed!'
                }
            })
@api_view(['GET',])
@authentication_classes([TokenAuthentication])
@permission_classes((IsAuthenticated,))
def user_detail(request, mobile_no):
    if request.method == "GET":
        #mobile_no = request.GET['mobile_no']
        if CustomUser.objects.filter(username=mobile_no, user_role=2).exists():
            print('1')
            user = CustomUser.objects.get(username=mobile_no)
            # print(user)
            print('2')
            login_object = LoginUser.objects.get(user_id=user)
            print(login_object)
            #if user:
                #token, created = Token.objects.get_or_create(user=user)
            return Response({
                "status": 200,
                "message": "success",
                "data":{
                    'first_name': user.first_name,
                    'phone_no': user.mobile_no,
                    'email': user.email,
                    'is_verified': user.is_verified,
                    'country' : login_object.country,
                    'user_profile': user.user_profile.url
                    
                }
            })
        else:
            return Response({
                "status": 400,
                "message": "failed",
                "data": {
                    "error_message": "user not found"
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
    # else:
    #             return Response({
    #                 "status": 400,
    #                 "message": "failed",
    #                 "data": {
    #                     "error_message": "Invalid.... user"
    #                 }
    #             })

                
# get customers
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes((IsAuthenticated,))
def get_customers(request):
    try:
        # custom_user_object = CustomUser.objects.get(user_id=request.user)
        # all_customer_request = customer.objects.filter(creator_id=custom_user_object.user_id)
        # c_list = []
        # for one in all_customer_request:
        #     c_list.append(one.user_id.pk)
        custom_object = CustomUser.objects.all()
        # customer_set = list(chain(all_customer_request, all_customer_objects))
        serializer = UserProfileSerializer(custom_object, many=True)
        return Response({
            "status": 200,
            "message": "success",
            "data": serializer.data
        })
    except:
        return Response({
            "status": 404,
            "message": "failed",
            "data": "fauhaa"
        })