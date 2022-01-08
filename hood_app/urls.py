from django.urls import path

from hood_app import views 

urlpatterns = [
    path('hoods',views.hood_view,name='neighbourhoods'),
    path('join_hood/<int:pk>',views.join_hood,name='join_hood'),
    path('my_hood/',views.get_hood,name='my_hood'),
    path('my_hood/<int:pk>',views.get_residents,name='get_residents'),
    path('move_out/',views.move_out,name='move_out'),
    path('business/',views.business_view,name='business'),
    path('business/<int:pk>',views.get_businesses,name='get_business'),
    path('search/<str:term>',views.search_business,name='search_business'),
    path('occurence/<int:pk>',views.occurence_view,name="occurence"),
    path('profile_pic',views.profile_pic,name='profile_pic')
]