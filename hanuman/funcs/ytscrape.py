import urllib.request
import re

def get_song_link(query):
    html = urllib.request.urlopen('https://www.youtube.com/results?search_query=' + query.replace(' ', '+'))
    all_links = re.findall(r"watch\?v=(\S{11})", html.read().decode())
    url = (f'https://www.youtube.com/watch?v={all_links[0]}')
    return url
