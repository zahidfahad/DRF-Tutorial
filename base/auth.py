import json
import jwt
from typing import Dict, List
from rest_framework.authentication import BaseAuthentication
from drf.settings import SECRET_KEY
from user.models import User
from base.caches import get_cache
from .exceptions import AuthenticationFailed



class TokenAuthentication(BaseAuthentication):
    auth_type = 'bearer'
    
    def authenticate(self, request):
        auth_header: str = request.headers.get('authorization')
        if not auth_header:
            return
        if auth_header:
            token_obj: List[str] = auth_header.split(' ')
            if len(token_obj) == 0:
                # Empty AUTHORIZATION header sent
                return None
            if token_obj[0].lower() not in ['bearer']:
                # Assume the header does not contain a bearer token
                raise AuthenticationFailed(
                    "Invalid token type",
                    code="invalid_token_type",
                )
            if len(token_obj) != 2:
                raise AuthenticationFailed(
                    "Authorization header must contain two space-delimited values",
                    code="bad_authorization_header",
                )
        try:
            payload = jwt.decode(jwt=token_obj[1], key=SECRET_KEY, algorithms='HS256', verify=True)
            if payload['token_type'].lower() != 'access':
                return AuthenticationFailed('No access token provided',code='no_access_token_found')
            user = self.get_user(payload)
            if not user:
                return AuthenticationFailed('can not retrieve user information',code='failed')
            setattr(request, 'user', user)
            return (user, token_obj[1])
        except Exception as e:
            raise AuthenticationFailed(f'{str(e)}')
            print(e)
        
    @staticmethod
    def get_user(data: Dict):
        try:
            try:
                user_data = json.loads(get_cache(f'{data["username"]}_token_data'))
            except Exception:
                raise AuthenticationFailed("User not found",code='not_found')
            user = User.objects.get(username__exact=user_data['username'])
            if not user.is_active:
                return
            return user
        except User.DoesNotExist:
            return
     
     
     
     
     

        
