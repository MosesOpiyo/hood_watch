from rest_framework import serializers

from .models import Hood,Business,Occurence,Profile
from hood_users.serializers import UserSerializer

class HoodSerializer(serializers.ModelSerializer):
    admin = UserSerializer(read_only=True)
    class Meta:
        model = Hood
        fields = '__all__'
    
    def save(self,request):
        profile = Profile.objects.get(user = request.user)
        hood = Hood(name=self.validated_data['name'],loation=self.validated_data['location'],admin = request.user,police_line=self.validated_data['police_line'],emergency_line=self.validated_data['emergency_line'])
        hood.save()
        profile = Profile.hood = hood
        profile.save()

class GetHoodSerializer(serializers.ModelSerializer):
    """This deals with parsing the neighbourhood model
    Args:
        serializers ([type]): [description]
    """
    admin = UserSerializer()
   
    class Meta:
        model = Hood
        fields = '__all__'
        read_only_fields = ['admin']

class BusinessSerializer(serializers.ModelSerializer):
    """This interchanges data pertaining the business class
    Args:
        serializers ([type]): [description]
    """
    owner = UserSerializer(read_only=True)
    class Meta:
        model = Business
        fields = '__all__'

    def save(self,request):
        business = Business(owner = request.user,name = self.validated_data['name'],services = self.validated_data['services'],image = self.validated_data['image'])

        business.save()

class OccurrenceSerializer(serializers.ModelSerializer):
    """This deals with parsing the occurences
    Args:
        serializers ([type]): [description]
    """
    reporter = UserSerializer(read_only=True)
    class Meta:
        model = Occurence
        fields = '__all__'
        read_only_fields = ['neighbourhood']

    def save(self,request,neighbourhood):
        occurence = Occurence(type = self.validated_data['type'],neighbourhood = neighbourhood,reporter = request.user, name = self.validated_data['name'],description = self.validated_data['description'],image_description = self.validated_data['image_description'])
        occurence.save()

class ProfileSerializer(serializers.ModelSerializer):
    neighbourhood = HoodSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    class Meta:
        model = Profile
        fields = '__all__'
