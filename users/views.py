from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

import requests

from .serializers import CreateUserSerializer

# Create your views here.

CLIENT_ID = 'p7i6kBolSZnKrAI3qU1CcoRJqNYAuBh6l40prBLR'
CLIENT_SECRET = 'KRvPif79X6dTbV1x9CideqDe07om64viT7YMjcNneVAZxSFGnw5KZdpaRpyUckFupzfeZA74un7gdHlRh9kg7IQQi4VMRQUHD710SQRl0:api_view(^)RlaFVGO9IMETNWrzMnEvJ4F'


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    '''
    Registers user to the server. Input should be in the format:
    {'username': 'username', 'password': 'secretpass123'}
    :param request:
    :return:
    '''

    # Put the data from the request into the serializer
    serializer = CreateUserSerializer(data=request.data)

    # Validate the data
    if serializer.is_valid():

        print("serializer is valid")

        # if it is valid, save the data (creates a user).
        serializer.save()

        print(f"username: {request.data['username']}")

        # then we get a token for the created user
        # this could be done differently
        r = requests.post('http://127.0.0.1:5002/o/token',
                          data={
                              'grant_type': 'password',
                              'username': request.data['username'],
                              'password': request.data['password'],
                              'client_id': CLIENT_ID,
                              'client_secret': CLIENT_SECRET,
                          })
        print(r.json())
        return Response(r.json())
    return Response(serializer.errors)


@api_view(['POST'])
@permission_classes([AllowAny])
def token(request):
    '''
    Gets tokens with username and password. Input should be in the format:
    {"username": "username", "password": "1234abcd"}
    '''
    r = requests.post(
        'http://127.0.0.1:5002/o/token/',
        data={
            'grant_type': 'password',
            'username': request.data['username'],
            'password': request.data['password'],
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
        },
    )
    return Response(r.json())


@api_view(['POST'])
@permission_classes([AllowAny])
def refresh_token(request):
    '''
    Registers user to the server. Input should be in the format:
    {"refresh_token": "<token>"}
    '''
    r = requests.post(
        'http://127.0.0.1:5002/o/token/',
        data={
            'grant_type': 'refresh_token',
            'refresh_token': request.data['refresh_token'],
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
        },
    )
    return Response(r.json())


@api_view(['POST'])
@permission_classes([AllowAny])
def revoke_token(request):
    '''
    Method to revoke tokens.
    {"token": "<token>"}
    '''
    r = requests.post(
        'http://127.0.0.1:5002/o/token/',
        data={
            'token': request.data['token'],
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
        },
    )
    # If it goes well return sucess message (would be empty otherwise)
    if r.status_code == requests.codes.ok:
        return Response({'message': 'token revoked'}, r.status_code)
    # Return the error if it goes badly
    return Response(r.json(), r.status_code)
