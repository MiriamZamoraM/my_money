from django.urls import path
from .views import RegistryView
from .views import ListApiView

urlpatterns = [
    path('registry/', RegistryView.as_view(), name="registro"),
    path('list/', ListApiView.as_view(), name="lista"),
]