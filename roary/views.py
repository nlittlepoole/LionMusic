from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect
import requests
import base64
import simplejson as json
# Create your views here.
def home(request):


    dict_context = {'message': 'Login'}
    if request.session.get('uni'):
        dict_context['uni'] = request.session['uni']
    return render(request, 'roary/index.html', dict_context, context_instance = RequestContext(request))
def player(request):


    dict_context = {'message': 'Login'}
    if request.session.get('uni'):
        dict_context['uni'] = request.session['uni']
    return render(request, 'roary/player2.html', dict_context)

def login(request):
    """
    Author: @niger
    Check uni and password against oath library and then add user data to User table
    """
    import oauth
    from roary.models import User

    uni = request.POST.get('uni','')
    password = request.POST.get('password','')

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
            print track
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