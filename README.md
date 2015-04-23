# SpottyPlaylistCreator
Create Spotify playlists from textfile lists (eg Google Music playlist exports)

NOTE: This script utilizes the "spotipy" python wrapper of libspotify. 
      https://github.com/plamere/spotipy
      To run SpottyPlaylistCreator you will need to install python and spotipy

The following steps are required to create a Spotify playlist using this program

1) Go to https://developer.spotify.com/my-applications to sign up for developer credentials
	note: you will need a spotify premium account to get them

2) set the following OS environment variables using your acquired credentials:
	SPOTIPY_CLIENT_ID,
 	SPOTIPY_CLIENT_SECRET,
	SPOTIPY_REDIRECT_URI,

3) Execute "python SpottyPlaylistCreator.py <username> <playlist_name> <input_txt>"
	eg: "python SpottyPlaylistCreator.py taubergm workout ExamplePlaylistText.txt"

4) follow the instructions in the console
	- navigate to the webpage printed in the console
	- enter the URL that you were directed to

5) Watch to see whether the playlist could be created and to see which songs were added to it
