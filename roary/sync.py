import soundcloud

def sound_cloud_link():
    client = soundcloud.Client(client_id='625ababca85331b09722e7b4ec160580',
                                   client_secret='e5a7c3e37c423e40191c12e6c5b46dc7',
                                   redirect_uri='http://127.0.0.1:8002/soundcloud/?success=true')

    # redirect user to authorize URL
    return client.authorize_url()
def sound_cloud_sync(code):
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
def google_music(gmail, psswd):

    from gmusicapi import Mobileclient
    api = Mobileclient()
    songs =[]

    if api.login(gmail, psswd):
        library = api.get_all_songs()

        for track in  library:
            song = {}
            song['name'] = track.get('title','')
            song['artist'] = track.get('artist','')
            song['year'] = track.get('year',0)
            song['genre'] = track.get('genre','')
            song['plays'] = track.get('playCount',0)
            songs.append(song)

    return songs
if __name__ == '__main__':
    gmail = raw_input('Gmail:\n')
    psswd = raw_input('Password:\n')

    songs =  google_music(gmail,psswd)
    print len(songs)