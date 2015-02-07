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
    success = request.GET.get('success',None)

    dict_context = {'message': 'Login'}
    if request.session.get('uni'):
        dict_context['uni'] = request.session['uni']
    if success:
        dict_context['fail'] = True
    return render(request, 'roary/index.html', dict_context, context_instance = RequestContext(request))
def player(request):

    if request.session.get('uni'):
        import radio
        song = radio.underground_track() if request.GET.get('station') else radio.top_track()
        dict_context = {'message': 'Login','track':song}
        dict_context['uni'] = request.session['uni']


        return render(request, 'roary/player2.html', dict_context)
    else:
        return redirect('/index')

def logout(request):

    if request.session.get('uni'):
        request.session['uni'] = None
    return redirect('/index')

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
        return redirect('/index') # Generic 200 response, replace with actual response later
    else:
        return redirect('/index?success=fail')
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
        return redirect('/index')

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
                a.art = song.get('art') if song.get('art') else a.art
                a.save()
            x.spotify_music_time = str(time.time())
        return redirect('/index')
    else:
        return redirect(sync.spotify_link())
def track(request):
    import simplejson as json
    import radio
    song = radio.underground_track() if request.GET.get('station') else radio.top_track()

    return HttpResponse(json.dumps(song))
