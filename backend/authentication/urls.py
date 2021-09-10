from django.urls import path, include
from .views import SocialSignupAPIView

urlpatterns = [
    path('socialSignup', SocialSignupAPIView.as_view(), name= social-signup),
]
