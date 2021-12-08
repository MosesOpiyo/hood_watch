from django.db import models
from django.db.models.deletion import CASCADE, SET_NULL
from django.db.models.signals import post_save
from django.dispatch import receiver
from cloudinary.models import CloudinaryField

from hood_users.models import Account

# Create your models here.
class Hood(models.Model):
    name = models.CharField(max_length=100,unique=True)
    location = models.CharField(max_length=200)
    admin = models.ForeignKey(Account,on_delete=SET_NULL)
    police_line = models.IntegerField(max_length=10)
    emergency_line = models.IntegerField(max_length=10)

class Occurence(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    reporter = models.ForeignKey(Account,on_delete=SET_NULL)
    hood = models.ForeignKey(Account,on_delete=CASCADE)
    time_reported = models.TimeField(auto_now_add=True)

class Business(models.Model):
    name = models.CharField(max_length=200)
    owner = models.ForeignKey(Account,on_delete=CASCADE)
    services = models.TextField()

    def delete_business(self):
        self.delete()
    
class Profile(models.Model):
    profile_pic = CloudinaryField(blank=True)
    user = models.ForeignKey(Account,on_delete=CASCADE,null=False)
    hood = models.ForeignKey(Hood,on_delete=SET_NULL)
    
    def get_residents(pk):
        """
        This will return all users in a given neighbourhood
        Args:
            pk ([type]): [description]
        Returns:
            [type]: [description]
        """
        hood = Hood.objects.get(pk=pk)
        users = Account.objects.filter(profile__hood = hood)
        return users

    @receiver(post_save, sender=Account)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=Account)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()