from django.db import models
from django.db.models.deletion import CASCADE, SET_NULL
from django.db.models.fields.related import OneToOneField
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

    def get_events(pk):
        """This returns all the events reported regarding a neighbourhood
        Args:
            pk ([type]): [description]
        """
        hood = Hood.objects.get(pk = pk)
        events = Occurence.objects.filter(hood = hood)

        return events

class Business(models.Model):
    name = models.CharField(max_length=200)
    owner = models.ForeignKey(Account,on_delete=CASCADE)
    services = models.TextField()

    def delete_business(self):
        self.delete()
    def get_bussinesses(pk):
        """This returns all businesses provided a neighbourhood
        Returns:
            [type]: [description]
        """
        hood = Hood.objects.get(pk=pk)
        
        owners = Account.objects.filter(profile__hood = hood)

        businesses = []
        for i in owners:
            try:
                business = Business.objects.get(owner = i)
                businesses.append(business)
            except:
                continue

        return businesses
    def search_by_name(search_term):
        """This returns a business after being fed a query term
        Args:
            search_term ([type]): [description]
        Returns:
            [type]: [description]
        """
        results = []
        businesses = Business.objects.filter(name__icontains = search_term)

        for business in businesses:
            results.append(business)

        return results
    
class Profile(models.Model):
    profile_pic = CloudinaryField(blank=True)
    user = OneToOneField(Account,on_delete=CASCADE,null=False)
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