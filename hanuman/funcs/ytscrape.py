import urllib.request
import re
import youtube_dl

def get_song_link(query):
    html = urllib.request.urlopen('https://www.youtube.com/results?search_query=' + query.replace(' ', '+'))
    all_links = re.findall(r"watch\?v=(\S{11})", html.read().decode())
    url = (f'https://www.youtube.com/watch?v={all_links[0]}')
    return url

def get_song_details(url):
    
    ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': 'tmp/%(id)s.%(ext)s',
    'noplaylist': True,
    'quiet': True,
    'prefer_ffmpeg': True,
    'audioformat': 'wav',
    'forceduration':True
}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        dictMeta = ydl.extract_info(url, download=False)
    
    return (dictMeta['title'], dictMeta['duration'])
