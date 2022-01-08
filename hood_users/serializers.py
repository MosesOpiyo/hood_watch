from rest_framework import serializers
from rest_framework.authtoken.models import Token

from hood_app.models import Profile

from .models import Account

class RegistrationSerializer(serializers.ModelSerializer):
    """This sets up the registration view with all its contents
    Args:
        serializers ([type]): [description]
    """
   

    class Meta:
        model = Account
        fields = ['email','username','password']
        extra_kwargs = {
            'password':{'write_only':True}
        }

    def save(self):
        account = Account(email = self.validated_data['email'],username = self.validated_data['username'])
        account.set_password(self.validated_data['password'])
        account.save()
        return account


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id','email','username','date_joined','last_login','profile_pic']

    def save(self):
        profile_pic = Account(profile_pic = self.validated_data['profile_pic'])
        profile_pic.save()
        return profile_pic