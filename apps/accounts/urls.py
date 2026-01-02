from django.urls import path
from .views import PostAccount, IDAccountAPIView

urlpatterns=[
    path('regpost/', PostAccount.as_view()),
    path('<int:pk>/', IDAccountAPIView.as_view()),
]