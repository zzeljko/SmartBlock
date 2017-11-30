from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^home', views.home_page, name='home'),
    url(r'^myprofile', views.my_profile, name='myProfile'),
]