# hanumanbot

##### for when they ban or shut down all the other bots and you just want something to work
<br>

# SETUP
- First, either download the repository or run the following command 
```git pull https://github.com/im-NL/hanumanbot.git```

- Install the dependencies required to run the project in `requirements.txt`. You can do this by running:
```pip install -r requirements.txt```

### NOTE
youtube_dl has to be installed separately, for this, run 
```pip install git+https://github.com/ytdl-org/youtube-dl.git@master#egg=youtube_dl```
This is because the latest youtube-dl version (as of 8th June 2023) does not work properly due to changes in YouTube itself. They have added a fix
for this in their master branch but the changes have not yet been reflected in the pip package.

### AUTH FILE **IMPORTANT** 
- Add your bot's `DISCORD TOKEN` as `token` in ``funcs/auth.py`` 
- Add your spotify application's `client` and `secret` as the client and secret variables in ``funcs/auth.py``. These will only be needed if you want the bot to be able to play from spotify links (either songs or playlists). If you don't mind writing out the song names yourself or don't wanna add a spotify playlist to queue then leave the strings empty, the bot will work without it as well.

### FFMPEG 
Download ffmpeg.exe from ``https://www.ffmpeg.org/download.html`` and save it in the hanumanbot folder

<br>

That's it! You should be able to run the bot now. There's a decent amount of setup so if you don't wanna set up the bot yourself then you can contact me and I'll send you the complete ready to run folder with ffmpeg etc. installed 

<img src="https://cdn.discordapp.com/app-icons/937028174322212905/a3f4592ffe6bd04fb438d6c79b8038f9.png">
