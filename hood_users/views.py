from rest_framework.decorators import APIView,api_view,permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken import views
import json

from .serializers import RegistrationSerializer
from .models import Account

@api_view(['POST'])
def registration_view(request):
    serializer = RegistrationSerializer(data=request.data)
    data = {}
    if serializer.is_valid():
        account = serializer.save()
        data['response'] = f"Successfully created a new user under {account.username}"
        return Response(data,status = status.HTTP_201_CREATED)
    else:
        data = serializer.errors
    

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

