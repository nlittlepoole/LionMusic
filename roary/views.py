from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect
# Create your views here.
def home(request):

    from roary.models import Song,Queue
    from django.db import models
    from django.db.models import Avg
    import time
    import math
    import random
    #while 1:
    # Code executed here
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
    for song in coordinates[:length] :
        print song


    #Song.objects.raw('SELECT * FROM SONG WHERE ')
    #time.sleep(300)
    dict_context = {'message': 'Login'}
    if request.session.get('uni'):
        dict_context['uni'] = request.session['uni']
    return render(request, 'roary/index.html', dict_context, context_instance = RequestContext(request))
def player(request):


    dict_context = {'message': 'Login'}
    if request.session.get('uni'):
        dict_context['uni'] = request.session['uni']
    return render(request, 'roary/player.html', dict_context)
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
    sync.google_music("nlittlepoole@gmail.com","naomipurnell")
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
    if not success:
        return redirect(sync.sound_cloud_link())
    else:
        code = request.GET.get('code')
        tracks = sync.sound_cloud_sync(code)
        for track in tracks:
            #print track
            4
        return HttpResponse(str(tracks))

def spotify(request):
    """
    Redirect to spotify login

    handle spotify oath and sync
    """

    import sync
    access_token = request.GET.get('code')
    if access_token:
        songs = sync.spotify_sync(access_token)
        return HttpResponse(str(songs))
    else:
        return redirect(sync.spotify_link())