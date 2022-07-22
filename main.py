# Credits: Brook Jeynes & Brady Stroud

import os
import json
import spotipy
import spotipy.util as util

def init():
    username = "username_here"
    scope = 'user-read-private user-read-playback-state user-modify-playback-state'

    try:
        token = util.prompt_for_user_token(username, scope, client_id='client_id_here',
                            client_secret='client_secret_here',
                            redirect_uri='http://localhost:8888/callback/')
    except:
        os.remove(f".cache={username}")
        token = util.prompt_for_user_token(username, scope, client_id='client_id_here',
                            client_secret='client_secret_here',
                            redirect_uri='http://localhost:8888/callback/')

    global spotifyObject
    spotifyObject = spotipy.Spotify(auth=token)


def backup():
    code = input("code: ")
    fileName = input("file name: ")
    length = spotifyObject.playlist_tracks(code, fields="total", offset=0, market=None, additional_types=('track', ))["total"] 
    # caps each loop to 100 songs due to spotify limit
    loopLimit = int(length / 100)
    offsetCounter = 0 

    for _ in range(loopLimit + 1):
        playlist = spotifyObject.playlist_tracks(code, fields="items(track(name, uri))", offset=offsetCounter, market=None, additional_types=('track', )) # GRAB SPOTIFY SONG TITLE AND URI
 
        f = open((fileName + ".txt"), "a") 
        f.write(json.dumps(playlist, indent=4)) # FORMATS DATA
        f.close()

        offsetCounter += 100 

def main():
  init()
  backup()

if __name__ == "__main__":
  main()
