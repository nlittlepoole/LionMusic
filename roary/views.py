from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect
import time
# Create your views here.
def home(request):




    #Song.objects.raw('SELECT * FROM SONG WHERE ')
    #time.sleep(300)
    dict_context = {'message': 'Login'}
    if request.session.get('uni'):
        dict_context['uni'] = request.session['uni']
    return render(request, 'roary/index.html', dict_context, context_instance = RequestContext(request))
def player(request):

    song = track()
    dict_context = {'message': 'Login','track':song}
    if request.session.get('uni'):
        dict_context['uni'] = request.session['uni']
    return render(request, 'roary/player2.html', dict_context)
def logout(request):

    if request.session.get('uni'):
        request.session['uni'] = None
    return HttpResponse("OK") #

def login(request):
    """
    Author: @niger
    Check uni and password against oath library and then add user data to User table
    """
    import oauth
    from roary.models import User

    uni = request.POST.get('uni','')
    password = request.POST.get('password','')
    import sync
    #sync.google_music("nlittlepoole@gmail.com","naomipurnell")
    data = oauth.login(uni,password)
    if data:
        user = User(uni = data['uni'], department = data['dept'], dorm = data['dorm'] )
        user.save()
        request.session['uni'] = uni
        return HttpResponse("OK") # Generic 200 response, replace with actual response later
    else:
        return HttpResponseBadRequest()
def sound_cloud(request):
    """
    Redirect to Sound Cloud login
    Handle soundcloud redirect
    """

    success = request.GET.get('success',None)
    # create client object with app credentials
    import sync
    from roary.models import Song,User
    if not success:
        return redirect(sync.sound_cloud_link())
    else:
        code = request.GET.get('code')
        uni = request.session.get('uni')
        logged_in = sum(1 for result in User.objects.filter(uni=uni)) > 0
        if logged_in:
            x = User.objects.filter(uni=uni)[0]
            stamp = x.soundcloud_music_time if x.soundcloud_music_time and x.soundcloud_music_time != '' else 0
            tracks = sync.sound_cloud_sync(code,float(stamp))
            for song in tracks:
                exists = sum(1 for result in Song.objects.filter(url=song['url'])) > 0

                a= Song(name=song['name'],url=song['url'],year=song['year'],genre=song['genre'],artist=song['artist']) if not exists else Song.objects.filter(url=song['url'])[0]
                a.duration= 0
                a.plays= song.get('plays',0) if not exists else a.plays+song['plays']
                a.users = 0 if not exists else a.users+1
                a.art = song.get('art') if song.get('art') else a.art
                a.save()
            x.soundcloud_music_time = str(time.time())
        return HttpResponse("ok")

def spotify(request):
    """
    Redirect to spotify login

    handle spotify oath and sync
    """

    import sync
    from roary.models import Song,User
    access_token = request.GET.get('code')
    uni = request.session.get('uni')
    if access_token and uni:
        logged_in = sum(1 for result in User.objects.filter(uni=uni)) > 0
        if logged_in:
            x = User.objects.filter(uni=uni)[0]
            stamp = x.spotify_music_time if x.spotify_music_time and x.spotify_music_time != '' else 0
            songs = sync.spotify_sync(access_token,float(stamp))
            for song in songs:
                exists = sum(1 for result in Song.objects.filter(url=song['url'])) > 0

                a= Song(name=song['name'],url=song['url'],year=song['year'],genre=song['genre'],artist=song['artist']) if not exists else Song.objects.filter(url=song['url'])[0]
                a.duration= 0
                a.plays= song.get('plays',0) if not exists else a.plays+song['plays']
                a.users = 0 if not exists else a.users+1
                a.save()
            x.spotify_music_time = str(time.time())
        return HttpResponse("OK")
    else:
        return redirect(sync.spotify_link())
def top_40(request):
    import simplejson as json
    song = track()
    return HttpResponse(json.dumps(song))
def track():
    from roary.models import Song,Queue
    from django.db import models
    from django.db.models import Avg
    import math
    import random


    tup = Song.objects.aggregate(average_plays=Avg('plays'),average_users=Avg('users'))
    avg_plays = tup.get('average_plays',0)
    avg_users = tup.get('average_users',0)

    print avg_plays,avg_users
    coordinates= []
    top_40 = Song.objects.raw('SELECT * FROM roary_song WHERE plays>= %s and users >= %s', [avg_plays,avg_users])
    for a in top_40:
        coordinate = {}
        coordinate['data'] = a
        coordinate['r'] =((avg_plays - a.plays)**2 + (avg_users - a.users)**2)**0.5
        coordinate['theta'] =  math.degrees(math.atan( (a.plays - avg_plays)/(a.users-avg_users + .001)  ))
        coordinate['rank'] = coordinate['r'] *(1-(abs(45-coordinate['theta'])/45))
        coordinates.append(coordinate)
    small = min([x['rank'] for x in coordinates])
    top = sorted(coordinates, key=lambda k: k['rank'])
    coordinates.sort(key = lambda item: random.random() * item['rank']/small)
    length = len(coordinates)/2 +1 if len(coordinates) < 10 else 10
    thing =  coordinates[0]
    track = thing['data']
    song = {}
    song['name'] = track.name
    song['artist'] = track.artist
    song['plays'] = track.plays
    song['genre'] = track.genre
    song['year'] =track.year
    song['url'] = track.url.split('v=')[1]
    song['art'] = track.art if track.art and track.art!='' else "https://c1.staticflickr.com/9/8206/8187575707_45abf81e2e_h.jpg"
    return song