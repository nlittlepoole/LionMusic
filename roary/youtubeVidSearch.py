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
    #print(content)
    artUrl = content['items'][0]['snippet']['thumbnails']['high']['url']
    print(artUrl)
    return [videoUrl, artUrl]

def titleCleaner(title):
    remix = False
    if 'remix' in title.lower():
        remix = True
    if '[' in title:
        openindex = title.index('[')
        closeindex = title.index(']')
        title = title[:openindex] + title[closeindex+1:]
    if '(' in title:
        openindex = title.index('(')
        closeindex = title.index(')')
        title = title[:openindex] + title[closeindex+1:]
    title = title.strip()
    if remix:
        title += ' Remix'
    return title

#t = titleCleaner('Forever is Ours (feat. Emma Hewitt) [Remix]')