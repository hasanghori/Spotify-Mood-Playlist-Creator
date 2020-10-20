import spotipy
from spotipy.oauth2 import SpotifyOAuth
from refreshToken import Refresh
from pprint import pprint
import requests
import json


class songObject:
    def __init__(self, uri, acousticness, danceability, energy, tempo,
                 valence):
        self.uri = uri
        self.acousticness = acousticness
        self.danceability = danceability
        self.energy = energy
        self.tempo = tempo
        self.valence = valence


def createObjectsList(songIDList, spotifyObject):
    songObjectsList = []
    for i in range(0, len(songIDList)):
        songFeatures = spotifyObject.audio_features(songIDList[i])
        songObj = songObject(songIDList[i], acousticness=songFeatures[0]['acousticness'],
                             danceability=songFeatures[0]['danceability'], energy=songFeatures[0]['energy'],
                             tempo=songFeatures[0]['tempo'], valence=songFeatures[0]['valence'])
        songObjectsList.append(songObj)
    return songObjectsList


def carVibes(songObj):
    carVibeness = int(songObj.tempo + (songObj.energy * 190) + (songObj.danceability * 190))
    return carVibeness


def sadBoiHours(songObj):
    sadBoiHoursNess = int(-(songObj.tempo * .9) - (songObj.energy * 180) - (songObj.danceability * 190)
                          - (songObj.valence * 200))
    return sadBoiHoursNess


def workout(songObj):
    workoutAbility = int((songObj.tempo * 1.5) + (songObj.energy * 190) + (songObj.danceability * 90))
    return workoutAbility


def vibeDecider(song, vibe):
    if vibe == 1:
        return carVibes(song)
    elif vibe == 2:
        return sadBoiHours(song)
    else:
        return workout(song)


def quickSort(songObjectsList, vibe):
    length = len(songObjectsList)
    if length <= 1:
        return songObjectsList
    else:
        pivot = songObjectsList.pop()

    songs_higher = []
    songs_lower = []

    for song in songObjectsList:
        if vibeDecider(song, vibe) > vibeDecider(pivot, vibe):
            songs_higher.append(song)
        else:
            songs_lower.append(song)

    return quickSort(songs_higher, vibe) + [pivot] + quickSort(songs_lower, vibe)


scope = ' '.join([
    'user-read-email',
    'playlist-read-private',
    'playlist-modify-private',
    'playlist-modify-public',
])

username = input("enter spotify username")

refreshToken = Refresh()
tokenBearer = refreshToken.refresh()
token = SpotifyOAuth(scope=scope, username=username)
spotifyObject = spotipy.Spotify(auth_manager=token)

#finding the playlist
playlistName = input("What is the playlist that you want to use?")
response = spotifyObject.user_playlists(user=username, limit=1)
numOfPlaylists = response['total']

count = int(0)

while (numOfPlaylists > count):
    if (playlistName == response['items'][0]['name']):
        break
    response = spotifyObject.user_playlists(user=username, limit=1, offset=count)
    count = count + 1
playlistID = response['items'][0]['id']


#finding and sorting tracks based on the vibe
playlist = spotifyObject.user_playlist_tracks(user=username, playlist_id=playlistID)
numberOfSongs = int(playlist['total'])
totalAdded = int(0)
songURIS = []
while (numberOfSongs > totalAdded):
    playlist = spotifyObject.user_playlist_tracks(user=username, playlist_id=playlistID,offset=totalAdded)
    for i in range(0, len(playlist['items'])):
        songURIS.append(playlist['items'][i]['track']['uri']) #id
    totalAdded = totalAdded + 100

songObjectsList = []
songObjectsList = createObjectsList(songIDList= songURIS, spotifyObject=spotifyObject)

print("what is the vibe of the sub playlist you want to create")
print("respond with 1 2 or 3")
vibe = input("1) car playlist 2) sad moody playlist 3) workout playlist")

#sorts songs and adds them to playlist
sortedSongsList = quickSort(songObjectsList, int(vibe))
numSongs = input("how many songs do you want in your playlist (max is 100)")
songsToAdd = []
print(len(sortedSongsList))
for songs in range(0, int(numSongs)):
    songsToAdd.append(sortedSongsList[songs].uri)

playlist_name = input("what do you want your new playlist to be called?")

spotifyObject.user_playlist_create(user=username, name=playlist_name, public=True)
prePlaylist = spotifyObject.user_playlists(user=username)
playlist = prePlaylist['items'][0]['id']

spotifyObject.user_playlist_add_tracks(user=username, playlist_id=playlist, tracks=songsToAdd)