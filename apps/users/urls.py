from django.urls import path
from rest_framework_simplejwt import views as jwt_views 
from .views import RegistryView
from .views import ListApiView
from .views import VerifyEmail
from .views import LoginAPIView

urlpatterns = [
    path('registry/', RegistryView.as_view(), name="registro"),
    path('list/', ListApiView.as_view(), name="lista"),
    path('verify/<str:token>', VerifyEmail.as_view(), name = "verify"),
    path('login/', LoginAPIView.as_view(), name="login"),
]