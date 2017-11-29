from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^home', views.home_page, name='home'),
    # url(r'^newsfeed', views.newsfeed_post, name='newsfeed_post'),
]