from bs4 import BeautifulSoup
import urllib2
from mechanize import Browser
import prettytable
import subprocess
import os


# Gets the url of the top result from Youtube for a specific title
def getyoutubeUrl(title):

    print title
    youtubeUrl = "https://m.youtube.com/results?q=" + title
    videos_file = urllib2.urlopen(youtubeUrl)
    videos = videos_file.read()
    videos_file.close()

    soup = BeautifulSoup(videos, 'html.parser')

    video = soup.find('div',attrs={'class':'yt-lockup-tile'})

    return "https://m.youtube.com/"+str(video.a['href'])


# Gets the top 100 songs list from BillBoard
def getTop100():

    url = "http://www.billboard.com/charts/hot-100"

    songs_file = urllib2.urlopen(url)
    songs = songs_file.read()
    songs_file.close()

    soup = BeautifulSoup(songs,'html.parser')

    songs_list = soup.find_all('div',attrs={'class':'chart-row__main-display'})

    songs = prettytable.PrettyTable(["SNo", "Current Week", "Title", "Artist", "Last Week"])

    sno = 1

    for song in songs_list:

        s = {}

        current_week = song.find('span',attrs={'class':'chart-row__current-week'}).text.strip(' \t\n\r')
        last_week = song.find('span',attrs={'class':'chart-row__last-week'}).text.strip(' \t\n\r').replace("Last Week: ","")
        title = song.find('h2', attrs={'class': 'chart-row__song'}).text.strip(' \t\n\r.')
        artist = song.find('h3', attrs={'class': 'chart-row__artist'})
        if not artist:
            artist = song.find('a', attrs={'class': 'chart-row__artist'}).text.strip(' \t\n\r')
        else:
            artist = artist.text.strip(' \t\n\r\"')

        s = [sno, current_week, title, artist, last_week]

        # print s

        songs.add_row(s)

        sno += 1

    print songs

    return songs


# Invokes getTop100 to get the playlist
songs = getTop100()

# Removes border from PrettyTable
songs.border = False

# Removes header from PrettyTable
songs.header = False

# Gets the required song no from the user which has to be played
song_no = raw_input("Enter no to be played:")

# Gets the title of the song which has to be played
title = songs[int(song_no)-1].get_string(fields=['Title'])

# Removes space, newlines and dot(.) from the title
title = title.strip(' \n\t\r.').replace(' ','')

# Gets the Youtube url of the desired song
youtubeUrl = getyoutubeUrl(title)

# print youtubeUrl

# Plays the Youtube video of the desired song in the user' VLC player
os.system("open -a VLC "+youtubeUrl)
