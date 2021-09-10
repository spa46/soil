from django.urls import path, include
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', include('rest_auth.urls')),
    path('register/', include('rest_auth.registration.urls')),
    # path("logout/", LogoutView.as_view(), name="logout")
]
