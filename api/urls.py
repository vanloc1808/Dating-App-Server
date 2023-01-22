from django.urls import path

from . import views
from .views import UserRegisterView, UserLoginView, UserPasswordForgotView

urlpatterns = [
    path('register', UserRegisterView.as_view(), name='register'),
    path('login', UserLoginView.as_view(), name='login'),
    path('forgot', UserPasswordForgotView.as_view(), name='forgot'),
]