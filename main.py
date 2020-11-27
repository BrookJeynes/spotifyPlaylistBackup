# ----------------------------#
#            CREDIT           #
# BROOK JEYNES + BRADY STROUD #
#-----------------------------#

#----------------------------------------#
# TO DO:                                 #
# - IMPORT FILE DATA TO SPOTIFY PLAYLIST #
#    - CREATE NEW USER PLAYLIST          #
#    - READ EACH URI FROM FILE           #
#    - ADD URI TO PLAYLIST               #
#----------------------------------------#


#-----------#
# VARIABLES #
#-----------#
import os
import json
import spotipy
import spotipy.util as util


#-----------#
# FUNCTIONS #
#-----------#

# INITIALISES EVERYTHING
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


# GRABS THE NAME OF SONG AND SONG CODE AND OUTPUTS IT TO A FILE
def backup():
    code = input("code: ")
    fileName = input("file name: ")
    length = spotifyObject.playlist_tracks(code, fields="total", offset=0, market=None, additional_types=('track', ))["total"] # GRABS LENGTH OF PLAYLIST

    loopLimit = int(length / 100) # DECIDES HOW MANY TIMES TO LOOP DUE TO LIMIT OF 100 SONGS PER REQUEST
    offsetCounter = 0 

    for _ in range(loopLimit + 1):
        playlist = spotifyObject.playlist_tracks(code, fields="items(track(name, uri))", offset=offsetCounter, market=None, additional_types=('track', )) # GRAB SPOTIFY SONG TITLE AND URI
 
        f = open((fileName + ".txt"), "a") # OUTPUTS DATA TO FILE
        f.write(json.dumps(playlist, indent=4)) # FORMATS DATA
        f.close()

        offsetCounter += 100 # INCREMENTS OFFSET COUNTER

# MAIN FUNCTION
def main():
    init()
    backup()


#--------------#
# MAIN PROGRAM #
#--------------#
if __name__ == "__main__":
    main()