from rest_framework import serializers
from rest_framework.authtoken.models import Token

from .models import Account

class RegistrationSerializer(serializers.ModelSerializer):
    """This sets up the registration view with all its contents
    Args:
        serializers ([type]): [description]
    """
    password2 = serializers.CharField(style={'input_type':"password"},write_only=True)

    class Meta:
        model = Account
        fields = ['email','username','password', 'password2']
        extra_kwargs = {
            'password':{'write_only':True}
        }

    def save(self):
        account = Account(email = self.validated_data['email'],username = self.validated_data['username'])

        if self.validated_data['password'] != self.validated_data['password2']:
            raise serializers.ValidationError({"password":"The passwords must match"})

        account.set_password(self.validated_data['password'])
        account.save()
        return account


class LoginSerializer(serializers.Serializer):
    """this defines the fields needed for login function
    Args:
        serializers ([type]): [description]
    """
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type':"password"},write_only=True)

    def validate_account(self):
        account = Account.objects.get(email = self.validated_data['email'])
        if Account.check_password(account,self.validated_data['password']):
            return account
        else:
            raise serializers.ValidationError({'account':'The account credentials are incorrect'})