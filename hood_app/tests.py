from django.test import TestCase
from hood_users.models import Account
from hood_app.models import *

class NeighbourhoodTestClass(TestCase):
    def setUp(self):
        self.admin = Account.objects.create_superuser(
            username='developer',
            password='password'
        )
        self.neighborhood = Hood(
            name='Test Neighbourhood', location='langata', police_line='0798765431',emergency_line='0787654321', admin_id=self.admin.id)

    def test_instance(self):
        self.assertTrue(isinstance(self.neighborhood, Hood))

    def test_save_method(self):
        self.neighbourhood.create_neigborhood()
        neighborhoods = Hood.objects.all()
        self.assertTrue(len(neighborhoods) > 0)

    def test_delete_method(self):
        self.neighborhood.create_neigborhood()
        self.neighborhood.delete()
        neighborhoods = Hood.objects.all()
        self.assertTrue(len(neighborhoods) == 0)


class PostTestClass(TestCase):
    def setUp(self):
        self.user = Account.objects.create_user(
            username='user1',
            password='password'
        )
        self.post = Occurence(name='Test Post', description='Test Content')

    def test_instance(self):
        self.assertTrue(isinstance(self.post, Occurence))

    def test_save_method(self):
        self.post.save()
        posts = Occurence.objects.all()
        self.assertTrue(len(posts) > 0)

    def test_delete_method(self):
        self.post.save()
        self.post.delete_post()
        posts = Occurence.objects.all()
        self.assertTrue(len(posts) == 0)