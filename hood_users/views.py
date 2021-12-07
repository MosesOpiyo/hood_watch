from rest_framework.decorators import APIView,api_view,permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken import views
import json

from .serializers import RegistrationSerializer,LoginSerializer
from .models import Account

@api_view(['POST'])
def registration_view(request):
    serializer = RegistrationSerializer(data=request.data)
    data = {}
    if serializer.is_valid():
        account = serializer.save()
        data['response'] = f"Successfully created a new user under {account.username}"
        token, created = Token.objects.get_or_create(user=account)
        data['token'] = token.key
    else:
        data = serializer.errors
    return Response(data)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_user(request,pk):
    """This handles the view of deleting a user 
    Args:
        request ([type]): [description]
        pk ([type]): [description]
    """
    data = {}
    account = Account.objects.get(pk = pk)
    if request.user == account:
        account.inactivate()
        data['response'] = f'The user account {account.username} has been deactivated.'
        return Response(data,status = status.HTTP_200_OK)
    else:
        data['response'] = "You are not authorized to do that."
        return Response(data,status = status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def login_user(request):
    """[summary]
    Args:
        request ([type]): [description]
    """
    serializer = LoginSerializer(data=request.data)
    data = {}
    
    if serializer.is_valid():
        try:
            account = serializer.validate_account()
            token, created = Token.objects.get_or_create(user=account)
            data['account'] = RegistrationSerializer(account).data
            data['token'] = token.key
            status_code = status.HTTP_200_OK
            return Response(data,status = status_code)

        except:
            data['response'] = "The account credentials were wrong!"
            status_code = status.HTTP_404_NOT_FOUND
            return Response(data,status = status_code)
    else:
        data['response'] = serializer.errors
        return Response(data,status=status.HTTP_500_INTERNAL_SERVER_ERROR)