from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/users/', include('users.urls')),
    path('api/v1/', include('profiles.urls')),
    path('api/v1/account/', include('accounts.urls'))
]
