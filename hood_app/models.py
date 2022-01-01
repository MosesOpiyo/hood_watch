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
    admin = models.OneToOneField(Account,on_delete=SET_NULL,null=True)
    police_line = models.CharField(max_length=10)
    emergency_line = models.CharField(max_length=10)

class Occurence(models.Model):
    name = models.CharField(max_length=3000)
    description = models.TextField(null=True)
    reporter = models.ForeignKey(Account,on_delete=SET_NULL,related_name='events_reporter',null=True)
    hood = models.ForeignKey(Hood,on_delete=CASCADE,related_name='reported_events')
    time_reported = models.TimeField(auto_now_add=True)

    def get_events(pk):
        """This returns all the events reported regarding a neighbourhood
        Args:
            pk ([type]): [description]
        """
        hood = Hood.objects.get(pk = pk)
        events = Occurence.objects.filter(hood = hood)

        return events

class Services(models.Model):
    name = models.CharField(max_length=500)
    description = models.TextField()

class Business(models.Model):
    name = models.CharField(max_length=200)
    owner = models.ForeignKey(Account,on_delete=CASCADE)
    services = models.ForeignKey(Services,on_delete=SET_NULL,null=True)

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
    """This extends the user model and provides an interface to connect to the neighbourhood class
    Args:
        models ([type]): [description]
    """
    user = models.OneToOneField(Account,null=False,related_name="profile",on_delete=models.CASCADE,)
    hood = models.ForeignKey(Hood,null=True,blank=True,on_delete=models.SET_NULL,related_name="user")

    def __str__(self):
        return self.user.username + "'s " + "profile"

    def get_residents(pk):
        """This will return all users in a given neighbourhood
        Args:
            pk ([type]): [description]
        Returns:
            [type]: [description]
        """
        hood = Hood.objects.get(pk=pk)
        users = Account.objects.filter(profile_hood = hood)

        return users

    @receiver(post_save, sender=Account)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=Account)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()
