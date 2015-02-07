__author__ = 'Siddharth'
import requests
import json

def youtubeVidSearch(artist, songName):
    baseurl = 'https://www.googleapis.com/youtube/v3/search?part=snippet&type=video&videoCategoryId=10&key=AIzaSyBCXVXUOcD8eYWwijCmxdDhlf5qiRBOfdY&q='
    query = artist + songName
    queryUrl = baseurl + query
    res = requests.get(queryUrl)
    content = json.loads(res.content.decode('utf-8'))
    videoUrl = 'https://www.youtube.com/watch?v='
    videoUrl += content['items'][0]['id']['videoId']
    return videoUrl

y = youtubeVidSearch('Bruno Mars', 'Uptown Funk')
print(y)