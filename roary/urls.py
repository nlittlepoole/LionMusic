from django.conf.urls import patterns, url
from roary import views

urlpatterns = patterns('',
        url(r'^$', views.home, name='home'),
        url(r'login', views.login, name='login'),
        url(r'soundcloud', views.sound_cloud, name='SoundCloud'),
        url(r'spotify', views.spotify, name='Spotify'),
        )
