from typing import Set
from rest_framework.decorators import APIView,api_view,permission_classes
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from rest_framework import status
from rest_framework import generics
from rest_framework.serializers import Serializer

from .serializers import *
from hood_users.serializers import *
from .models import *


import json
# Create your views here.

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def hood_view(request):
    data = {}

    if request.method == 'GET':
        hoods = Hood.objects.all()
        data = GetHoodSerializer(hoods,many=True).data
        
        return Response(data,status = status.HTTP_200_OK)

    elif request.method == 'POST':
         serializer = HoodSerializer(data = request.data)
         if serializer.is_valid():
            serializer.save(request)
            data['success'] = "Hood was created successfully"
            return Response(data,status = status.HTTP_201_CREATED)

         else:
            data = serializer.errors
            return Response(data,status = status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def join_hood(request,pk):
    data = {}

    profile = Profile.objects.get(user = request.user)
    new_hood = Hood.objects.get(pk=pk)
    profile.hood = new_hood
    profile.save()
    data['success'] = f"Welcome to  {new_hood.name}."
    return Response(data,status = status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def move_out(request):
    data = {}
    profile = Profile.objects.get(user = request.user)
    profile.hood = None
    profile.save()
    data['success'] = "You are no longer a member of the neighbourhood!"
    return Response(data,status = status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_hood(request):
    data = {}
    profile = Profile.objects.get(user = request.user)
    print(profile.hood)
    data = ProfileSerializer(profile).data
    return Response(data,status = status.HTTP_200_OK)

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def business_view(request):
    data = {}

    if request.method == 'GET':
        businesses = Business.objects.all()
        data = BusinessSerializer(businesses,many=True).data

        return Response(data,status = status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = BusinessSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save(request)
            data['success'] = "New business successfully created."
            print(data)
            return Response(data,status=status.HTTP_201_CREATED)

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def occurence_view(request,pk):
    data = {}
    
    try:
        hood = Hood.objects.get(pk=pk)
    except :

        data['not found'] = "The neighbourhood was not found"
        return Response(data,status = status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        serializer = OccurrenceSerializer(data = request.data)

        if serializer.is_valid():
            serializer.save(request,hood)
            data['success'] = "The occurrence was successfully reported"
            return Response(data,status = status.HTTP_200_OK)

        else:
            data = serializer.errors
            print(data)
            return Response(data,status = status.HTTP_400_BAD_REQUEST)

    elif request.method == 'GET':
        occurences = Occurence.get_events(pk)
        data = OccurrenceSerializer(occurences,many=True).data

        return Response(data,status= status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_businesses(request,pk):
    """The view for getting all businesses in a neighbourhood
    Args:
        request ([type]): [description]
        pk ([type]): [description]
    """
    businesses = Business.get_bussinesses(pk)
    data = {}
    data['businesses'] = BusinessSerializer(businesses,many=True).data

    return Response(data,status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_residents(request,pk):
    """
    This parses the request to get the users in a certain neighbourhood
    Args:
        request ([type]): [description]
        pk ([type]): [description]
    """
    data = {}
    residents = Profile.get_residents(pk)
    data['residents'] = UserSerializer(residents,many=True).data
    return Response(data,status = status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_business(request,term):
    """This parses the view request for getting the businesses via a search term
    Args:
        request ([type]): [description]
    """
    data = {}

    results = Business.search_by_name(term)

    data['businesses'] = BusinessSerializer(results,many=True).data
    return Response(data,status=status.HTTP_200_OK)

@api_view(['POST'])
def profile_pic(request):
    data = {}
    if request.method == 'POST':
     serializer = PicSerializer(data = request.data)
     if serializer.is_valid():
        data['success'] = "Profile pic successfully changed."
        return Response(data,status=status.HTTP_201_CREATED)
    if request.method == 'GET':
        profile = Profile.objects.get(user =request.user)
        data['profile_pic'] = ProfileSerializer(profile).data
    return Response(data,status = status.HTTP_200_OK)
