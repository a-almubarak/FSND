import json
from flask import request, _request_ctx_stack,abort
from functools import wraps
from jose import jwt
from urllib.request import urlopen


AUTH0_DOMAIN = 'capstone-fsnd.eu.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'capstone'

## AuthError Exception
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


## Auth Header

def get_token_auth_header():
    auth = request.headers.get('Authorization',None)
    # print('auth equals to->')
    # print(auth)
    if auth is None:
        raise AuthError({
            'code':'authorization_header_missing',
            'description':'Authorization header is excpected'
            },401)
    data = auth.split()
    if data[0].lower() != 'bearer':
        raise AuthError({
            'code':'invalid_header',
            'description':'Authorization header must start with "Bearer" '
            },401)
    if len(data) == 1:
        raise AuthError({
            'code':'invalid_header',
            'desctiption':'Token not found'},401)
    if len(data) >2:
        raise AuthError({
            'code':'invalid_header',
            'description':'Authorization header must be Bearer'},401)
    token = data[1]
    return token

   

def check_permissions(permission, payload):
    if 'permissions' not in payload:
        raise AuthError({
            'code':'invalid_permission',
            'description':'Unable to find permissions in JWT'},403)
    if permission not in payload['permissions']:
        raise AuthError({
            'code':'unprocessable',
            'description':'Permission not found'},403)   
    return True

def verify_decode_jwt(token):
    url = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    keys = json.loads(url.read())
    unvirified_header = jwt.get_unverified_header(token)
    rsa_key={}
    for key in keys['keys']:
        if key['kid'] == unvirified_header['kid']:
            rsa_key = {
                    'kty': key['kty'],
                    'kid': key['kid'],
                    'use': key['use'],
                    'n': key['n'],
                    'e': key['e']
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                    token,
                    rsa_key,
                    algorithms=ALGORITHMS,
                    audience=API_AUDIENCE,
                    issuer=f'https://{AUTH0_DOMAIN}/'
                    )
            return payload
        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)
    raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
            }, 403)


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(*args, **kwargs)

        return wrapper
    return requires_auth_decorator