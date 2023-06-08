# HanumanBot

##### For when they ban or shut down all the other bots and you just want something to work
<br>

# FEATURES
> Music Playing- YouTube prevented bots from playing music in discord voice channels so there aren't any big bots doing it anymore, that's why I made this write $play \<song name> and the bot will join the VC you're in and play the song. Supports SPOTIFY PLAYLISTS, youtube links, and regular song names as well (there are obviously also other commands like pause, queue, skip etc. it has everything you'd need)

>TTS- $tts \<stuff you wanna say> will convert text to speech and say it in the VC. Clutch for when you don't want people around you hearing what you're saying.

>Memes- $meme top-text | bottom-text [with an image attatched] will send an image back with the text written on it.

>Misc- Some other useful commands like echo, setstatus (set's the bot's status) and purge

<br>

# SETUP
- First, either download the repository or run the following command 
```
git git pull https://github.com/im-NL/hanumanbot.git
```

- Install the dependencies required to run the project in `requirements.txt`. You can do this by running:
```
pip install -r requirements.txt
```
#

## **NOTE**
youtube_dl has to be installed separately, for this, run:
```
pip install git+https://github.com/ytdl-org/youtube-dl.git@master#egg=youtube_dl
```
This is because the latest youtube-dl version (as of 8th June 2023) does not work properly due to changes in YouTube itself. They have added a fix
for this in their master branch but the changes have not yet been reflected in the pip package.

#

## **AUTH FILE** \**(important)**
- Add your bot's `DISCORD TOKEN` as `token` in ``funcs/auth.py`` 
- Add your spotify application's `client` and `secret` as the client and secret variables in ``funcs/auth.py``. <br><br>
These will only be needed if you want the bot to be able to play from spotify links (either songs or playlists). If you don't mind writing out the song names yourself or don't wanna add a spotify playlist to queue then leave the strings empty, the bot will work without it as well.
#
## **FFMPEG** 
Download ffmpeg.exe from ``https://www.ffmpeg.org/download.html`` and save it in the hanumanbot folder.

#

That's it! You should be able to run the bot now. There's a decent amount of setup so if you don't wanna set up the bot yourself then you can contact me and I'll send you the complete ready to run folder with ffmpeg etc. installed.

