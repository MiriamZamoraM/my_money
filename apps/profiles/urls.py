from django.urls import path
from rest_framework_simplejwt import views as jwt_views 
from .views import PostAPIView

urlpatterns = [
    path('profile/', PostAPIView.as_view()),
]