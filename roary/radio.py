def top_track():
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
def underground_track():
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
    top_40 = Song.objects.raw('SELECT * FROM roary_song WHERE plays>= %s and users <= %s', [avg_plays,avg_users])
    for a in top_40:
        coordinate = {}
        coordinate['data'] = a
        coordinate['r'] =((avg_plays - a.plays)**2 + (avg_users - a.users)**2)**0.5
        coordinate['theta'] =  math.degrees(math.atan( (a.plays - avg_plays)/(a.users-avg_users + .001)  ))
        coordinate['rank'] = coordinate['r'] *(1-(abs(45+coordinate['theta'])/45))
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