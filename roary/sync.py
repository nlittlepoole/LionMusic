import soundcloud
import datetime
import time
def sound_cloud_link():
    client = soundcloud.Client(client_id='625ababca85331b09722e7b4ec160580',
                                   client_secret='e5a7c3e37c423e40191c12e6c5b46dc7',
                                   redirect_uri='http://127.0.0.1:8002/soundcloud/?success=true')

    # redirect user to authorize URL
    return client.authorize_url()
def sound_cloud_sync(code, last_sync = 0):
        client = soundcloud.Client(client_id='625ababca85331b09722e7b4ec160580',
                                   client_secret='e5a7c3e37c423e40191c12e6c5b46dc7',
                                   redirect_uri='http://127.0.0.1:8002/soundcloud/?success=true')
        # exchange authorization code for access token

        access_token = client.exchange_token(code)

        # make an authenticated call
        id = client.get('/me').id

        tracks = client.get('/me/favorites', limit=10000) #favorite(likes)
        playlists = client.get('/me/playlists') # list of playlists
        for playlist in playlists:
            tracks.extend(playlist.tracks)
        test = ''
        songs = []
        for track in tracks:
            #two formats of tacks, so ternary operator depending on if its a dict or an object
            stamp =  track.get('created_at') if type(track) == dict else track.created_at
            stamp = time.mktime(datetime.datetime.strptime(stamp[:-6].strip(), "%Y/%m/%d %H:%M:%S").timetuple())
            if stamp> last_sync:
                song = {}
                song['name'] = track.get('title') if type(track) == dict else track.title
                song['artist'] = '' #Soundcloud puts artist data in the name of the track

                if len(song['name'].split('-')) >1:
                    song['artist'] = song['name'].split('-')[0]
                    song['name'] = song['name'].split('-')[1]

                song['year'] = track.get('release_year',0) if type(track) == dict else track.release_year
                song['year'] = song['year'] if song['year'] != None else 0

                song['genre'] = track.get('genre','') if type(track) == dict else track.genre
                song['genre'] = song['genre'] if song['genre'] != None else ''

                # SoundCloud depreciated plays per user api call, so have to estimate based on total play count
                tot_plays = track.get('playback_count',1) if type(track) == dict else track.playback_count
                tot_plays = 2.0*tot_plays if tot_plays else 1

                tot_users = track.get('favoritings_count',1) if type(track) == dict else track.favoritings_count
                tot_users = 3.0*tot_users if tot_users else tot_plays

                song['plays'] = int(tot_plays/tot_users)
                songs.append(song)
        return songs
def spotify_link():
    login = 'https://accounts.spotify.com/authorize?client_id=f5388af5ad814472bce04c92edc81e50&response_type=code&redirect_uri=http://localhost:8002/spotify&scope=user-library-read playlist-read-private'
    return login
def spotify_sync(access_token,last_sync=0):
    import requests

    # oauth to get access token
    payload = {'grant_type': "authorization_code", 'code': access_token, 'redirect_uri': 'http://localhost:8002/spotify', 'client_id':'f5388af5ad814472bce04c92edc81e50' ,'client_secret':'48e640b0c6544cfca29997d6b1a9e7a8'}
    r = requests.post("https://accounts.spotify.com/api/token", data=payload)
    token = r.json().get('access_token')

    # deal with "your music"
    api_request = "https://api.spotify.com/v1/me/tracks"
    payload = {'Authorization': 'Bearer ' + token}
    r = requests.get(api_request,headers=payload)
    songs = []
    for dic in r.json().get('items'): # spotify api calls are returned as json
        stamp = dic.get("added_at")[:10]
        stamp = time.mktime(datetime.datetime.strptime(stamp, "%Y-%m-%d" ).timetuple())
        if stamp>last_sync:
            track=dic.get('track')
            song = {}
            song['name'] = track.get('name','')
            song['artist'] = ' '.join([x['name'] for x in track.get('artists',[])])
            song['plays'] = track.get('popularity',1)
            song['genre'] = '' # spotify doesn't have an endpoint in their api for genre
            song['year'] = 0 # spotify doesn't have an endpoint in their api for song year
            songs.append(song)
    #get user id
    api_request = "https://api.spotify.com/v1/me/"
    r = requests.get(api_request,headers=payload)
    uid= r.json().get('id')

    #get list of playlists associated with user
    api_request = "https://api.spotify.com/v1/users/" + uid + "/playlists"
    r = requests.get(api_request,headers=payload)
    playlists = r.json()

    #for each playlist, get all tracks and add to total list
    for playlist in playlists.get('items'):
        id = playlist.get('id')
        api_request = "https://api.spotify.com/v1/users/" + uid + "/playlists/"+id+"/tracks"
        r = requests.get(api_request,headers=payload)
        for dic in r.json().get('items'):
            stamp = dic.get("added_at")[:10]
            stamp = time.mktime(datetime.datetime.strptime(stamp, "%Y-%m-%d" ).timetuple())
            if stamp>last_sync:
                track=dic.get('track')
                song = {}
                song['name'] = track.get('name','')
                song['artist'] = ' '.join([x['name'] for x in track.get('artists',[])])
                song['plays'] = track.get('popularity',1) # imputing playcount to popularity rating [0,100]
                song['genre'] = '' # spotify doesn't have an endpoint in their api for genre
                song['year'] = 0 # spotify doesn't have an endpoint in their api for song year
                songs.append(song)

    return songs

def google_music(gmail, psswd,last_sync = 0):

    from gmusicapi import Mobileclient
    api = Mobileclient()
    songs =[]

    if api.login(gmail, psswd, ):
        library = api.get_all_songs()

        for track in  library:
            song = {}
            song['name'] = track.get('title','')
            song['artist'] = track.get('artist','')
            song['year'] = track.get('year',0)
            song['genre'] = track.get('genre','')
            song['plays'] = track.get('playCount',0)
            stamp = int(track.get('creationTimestamp',0))/1000.0
            if stamp > last_sync :
                songs.append(song)
                print track

    return songs
if __name__ == '__main__':
    gmail = raw_input('Gmail:\n')
    psswd = raw_input('Password:\n')

    songs =  google_music(gmail,psswd)
    print len(songs)