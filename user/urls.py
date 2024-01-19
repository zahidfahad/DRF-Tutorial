from django.urls import path
from user.views import (
    login,
    check_authentication
)

urlpatterns = [
    path('login/', login, name='login'),
    path('check-auth/', check_authentication, name='check_authentication')
]
