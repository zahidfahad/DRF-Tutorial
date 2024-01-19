import json
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    ListCreateAPIView,
    RetrieveUpdateAPIView,
    RetrieveDestroyAPIView,
    RetrieveUpdateDestroyAPIView   
)
from rest_framework import viewsets
from rest_framework.decorators import api_view,permission_classes
from base.caches import get_cache,set_cache,delete_cache
from base.tokens import create_tokens
from django.contrib.auth import authenticate
from .serializers import UserTokenSerializer
from rest_framework.permissions import AllowAny

# Create your views here.


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request, username=username,password=password)
    if user:
        access_token, refresh_token = create_tokens(user)
        set_cache(
            key=f'{user.username}_token_data', 
            value=json.dumps(UserTokenSerializer(user).data), 
            ttl=5*60*60
        )
        response = {
            "access_token": access_token,
            "refresh_token": refresh_token
        }
        return Response(response,status=status.HTTP_200_OK)
    else:
        return Response("No user found")
    
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def check_authentication(request):
    return Response("success")
