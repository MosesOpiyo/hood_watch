from django.urls import path

from hood_users import views as user_views
from rest_framework.authtoken import views
from rest_framework.authtoken import views as special_views


urlpatterns = [
    path('register',user_views.registration_view,name="register"),
    path('login', special_views.obtain_auth_token),
    path('delete/<int:pk>',user_views.delete_user,name="delete"),
]
