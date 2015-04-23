# SpottyPlaylistCreator
# author: Michael Tauberg
#         tauberg@gmail.com
# specify a spotify user account, a playlist name, and a source text file to
# create a new spotify playlist from the text list


import spotipy
import spotipy.util as util
import sys
import pprint
import os
import subprocess
import re

if len(sys.argv) > 3:
    username = sys.argv[1]
    playlistName = sys.argv[2]
    playlistFile = sys.argv[3]
else:
    print "Usage: %s <username> <playlist-name> <playlist_tracks_file>" % (sys.argv[0],)
    sys.exit()

token = util.prompt_for_user_token(username)

# 1) Check that the user-specified playlist file exists
if os.path.exists(playlistFile):
   with open(playlistFile, 'rb') as f:
       try:
           playlist = f.readlines()
           f.close()
       except : 
           print "could not open file " + playlistfile
           sys.exit()
else:
    print "could not find file " + playlistfile
    sys.exit()

# 2) Check that the username provided gives us a proper token
#   if yes, create the playlist
token = util.prompt_for_user_token(username)

playlist_id = ""
if token:
    sp = spotipy.Spotify(auth=token)
    sp.trace = False
    print "Creating paylist " + str(playlistName) + " ..."
    playlists = sp.user_playlist_create(username, playlistName)
    #pprint.pprint(playlists)
    playlist_id = playlists['id']
else:
    print "Can't get token for", username
    sys.exit()


# 3) Parse the Playlist file
foundTracks = []
missedTracks = []
numMissed = 0
numFound = 0

for line in playlist:
    line = line.lower()
    # Replace common music file extensions - this will throw off Spotify search
    line = line.replace(".mp3", "");
    line = line.replace(".aac", "");
    line = line.replace(".wav", "");
    line = line.replace(".wma", "");
    line = line.replace(".ogg", "");
    line = line.replace(".m4p", "");
    line = line.replace(".flac", "");
    # Remove numbers - this will throw off Spotify search (eg track nums)
    line = filter(lambda c: not c.isdigit(), line)
    # Remove items in parentheses - this will throw off Spotify search 
    line = re.sub(r'\([^)]*\)', '', line)
    line = re.sub(r'\[[^)]*\]', '', line)
    # Remove superfluous info between '-'s
    line = re.sub(r'\-[^)]*\-', '', line)
    # Replace underscores with spaces 
    line = re.sub(r'_', ' ', line)
    
    # Search for the song using cleaned string
    result = sp.search(line)

    try:
        trackUri = result['tracks']['items'][0]['uri']  # see if track found
    except:
        missedTracks.append(line)
        numMissed = numMissed + 1 
    else:
        track = sp.track(trackUri)
        foundTracks.append(track)
        numFound = numFound + 1 

print "Found " + str(numFound) + " tracks" 
print "Missed " + str(numMissed) + " tracks" 
print "Will try to find missing tracks in Spotify..."

# Try one last time to find missed trakcs
#   Use only the last part of the string and hope for the best
for track in missedTracks: 
    # Try splitting by '-' and search the last substring (presumably the song name)
    tokens = track.split('-')
    try:
        search_str = tokens[len(tokens)-1]
        result = sp.search(search_str)
    except:
        pass
    try:
        trackUri = result['tracks']['items'][0]['uri']  # see if track found
    except:
        pass 
    else:
        track = sp.track(trackUri)
        foundTracks.append(track)
        numFound = numFound + 1 
        missedTracks.pop()

for track in missedTracks:
    # Try splitting by '/' and search the last substring (presumably the song name)
    tokens = track.split('/')
    try:
        search_str = tokens[len(tokens)-1]
        result = sp.search(search_str)
    except:
        pass 
    try:
        trackUri = result['tracks']['items'][0]['uri']  # see if track found
    except:
        pass 
    else:
        track = sp.track(trackUri)
        foundTracks.append(track)
        numFound = numFound + 1 

print "Found a total of " + str(numFound) + " tracks in playlist file"


# 4) Get tracks and add them to our created playlist
index = 0
track_ids = [] 
for track in foundTracks:
    trackName = track['name']
    artistName = track['artists'][0]['name']
    trackUrl = track['external_urls']
    track_ids.append(track['id'])
    index = index + 1
    print str(index) + " - " + artistName + " - " + trackName
    
# Add the tracks!
print "Adding the tracks.."
results = sp.user_playlist_add_tracks(username, playlist_id, track_ids)

print "Complete."
    

