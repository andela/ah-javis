from django.urls import path

from .views import (
    LoginAPIView, RegistrationAPIView, UserRetrieveUpdateAPIView, VerifyAccount
)

app_name = "authentication"

urlpatterns = [
<<<<<<< HEAD
    path('user/', UserRetrieveUpdateAPIView.as_view(), name="update_user"),
    path('users/', RegistrationAPIView.as_view(), name="registration"),
    path('users/login/', LoginAPIView.as_view(), name="login"),
    path('users/verify/<uidb64>/<token>/',
         VerifyAccount.as_view(), name="verify"),
=======
    url(r'^user/?$', UserRetrieveUpdateAPIView.as_view(), name="user"),
    url(r'^users/?$', RegistrationAPIView.as_view(), name="registration"),
    url(r'^users/login/?$', LoginAPIView.as_view(), name="login"),
>>>>>>> 51a64b03fd9bf0b9b818e32a80662898d7f2acd2
]
