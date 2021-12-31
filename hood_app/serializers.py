from rest_framework import serializers

from .models import Hood,Business,Occurence,Profile, Services
from hood_users.serializers import UserSerializer

class HoodSerializer(serializers.ModelSerializer):
    admin = UserSerializer(read_only=True)
    class Meta:
        model = Hood
        fields = '__all__'
    
    def save(self,request):
        profile = Profile.objects.get(user = request.user)
        hood = Hood(name=self.validated_data['name'],location=self.validated_data['location'],admin = request.user,police_line=self.validated_data['police_line'],emergency_line=self.validated_data['emergency_line'])
        hood.save()
        profile.hood = hood
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
        business = Business(owner = request.user,name = self.validated_data['name'])

        business.save()

class ServiceSerializer(serializers.Serializer):
    """This deals with parsing the services
    Args:
        serializers ([type]): [description]
    """
    class Meta:
        model = Services
        fields = '__all__'

    def save(self):
        services = Services(name = self.validated_data['service'],description = self.validated_data['service_description'])

class OccurrenceSerializer(serializers.ModelSerializer):
    """This deals with parsing the occurences
    Args:
        serializers ([type]): [description]
    """
    reporter = UserSerializer(read_only=True)
    class Meta:
        model = Occurence
        fields = '__all__'
        read_only_fields = ['hood']

    def save(self,request,hood):
        occurence = Occurence(hood = hood,reporter = request.user, name = self.validated_data['name'],description = self.validated_data['description'])
        occurence.save()

class ProfileSerializer(serializers.ModelSerializer):
    hood = HoodSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    class Meta:
        model = Profile
        fields = '__all__'
