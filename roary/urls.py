from django.conf.urls import patterns, url
from roary import views

urlpatterns = patterns('',
        url(r'^index', views.home, name='home'),
        url(r'^$', views.home, name='home'),
        url(r'login', views.login, name='login'),
        url(r'soundcloud', views.sound_cloud, name='SoundCloud'),
        url(r'spotify', views.spotify, name='Spotify'),
        url(r'player', views.player, name='Player'),
        url(r'logout', views.logout, name='Logout'),
        url(r'track', views.track, name='Top40'),
        )
