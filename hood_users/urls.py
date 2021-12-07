from django.urls import path

from hood_users import views as user_views
from rest_framework.authtoken import views


urlpatterns = [
    path('register',user_views.registration_view,name="register"),
    path('login',user_views.login_user,name="login"),
    path('delete/<int:pk>',user_views.delete_user,name="delete"),
]
