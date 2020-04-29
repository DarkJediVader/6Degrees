import sys
import spotipy
import spotipy.util

from optparse import OptionParser

client_id = None
client_secret = None
redirect_uri = None
degrees = 1
playlist_name = '{0}Degrees of {1}'

def main_loop():
    user = input('Username: ').strip()
    scope = 'playlist-modify-public'

    token = spotipy.util.prompt_for_user_token(user, scope, client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri)
    if token:
        spotify = spotipy.Spotify(auth=token)

        go = True
        while go:
            six_degrees(spotify)

            go = input('Continue? (y/n): ') == 'y'
    else:
        print ('Can\'t get token for \'{0}\''.format(user))



"""
Main caller for generating a 6Degrees playlist
"""
def six_degrees(spotify):
    artist = input('Artist Name: ').strip()
    track_ids = artist_and_related_top_10(spotify, artist, degrees)
    playlist_id = create_or_update_playlist(spotify, artist)
    add_to_playlist(spotify, playlist_id, track_ids)

def top_10_of(spotify, artist):
    select_artist(spotify, artist)

"""
Get user to choose which artist seems to be the one they want
"""
def select_artist(spotify, artist):
    q = 'artist:' + encode(artist)
    artist_objs = (spotify.search(q, type='artist')['artists'])['items']
    if not artist_objs:
        print ('No results found.')
        six_degrees(spotify)

    print ('Please select the artist you want by enterting the number next to them.')

    option = 1
    artist_ids = []
    for artist in artist_objs:
        print ('{0}. Name: {1}, Genres: {2}, Link: {3}'.format(option, artist['name'], artist['genres'], (artist['external_urls'])['spotify']))
        artist_ids.append(artist['id'])
        option += 1

    artist_id = None
    while True:
        try:
            choice = int(input('Selection: '))
            if choice > 0 and choice < len(artist_ids) + 1:
                artist_id = artist_ids[choice]
                break
            else:
                print ('Selection must be between 1 and {0}'.format(len(artist_ids)))
        except:
            print('Input is not a number between 1 and {1}.'.format(choice, len(artist_ids)))

    return artist_id

def artist_and_related_top_10(spotify, artist, degrees):
    top_10_of(spotify, artist)

def add_to_playlist(spotify, playlist_id, track_ids):
    pass

"""
Replace all spaces with plus for query
"""
def encode(s):
    result = ''
    for c in s:
        if c == ' ':
            result += '+'
        else:
            result += c
    return result

"""
If a playlist for the artist already exists return it, otherwise create a new
one to add the songs to.
"""
def select_playlist(spotify, artist, user_id):
    user_playlists = spotify.current_user_playlists()
    playlist_name = '{0}Degrees of {1}'.format(degrees, artist)

    playlist_id = None
    for playlist in user_playlists['items']:
        if playlist['name'] == playlist_name:
           playlist_id = playlist['id']

    if not playlist_id:
        playlist_id = spotify.user_playlist_create(user_id, playlist_name, True, 'Created by 6Degrees')

    return playlist_id


def create_or_update_playlist(spotify, artist):
    user_id = spotify.current_user()['id']
    playlist_id = select_playlist(spotify, artist, user_id)

"""
Parse args for the program. First must be sid filename, remaining are optional.
"""
def parse_args(args):
    usage = 'usage: {0} <sid_file> [options]'
    if len(args) > 1:
        filename = args[1]

        parser = OptionParser(usage=usage.format('%prog'))
        parser.add_option('-d', '--Degrees', default=1, dest='degrees', type='int', help='Set how many layers deep the application goes. The higher the number the longer the runtime and larger the playlist.')

        (options, args) = parser.parse_args()

        global degrees
        degrees = options.degrees

        parse_sid(filename)
    else:
        print (usage.format(args[0]))
        sys.exit()

"""
Set the client id and client secret found in the file specified by filename
"""
def parse_sid(filename):
    if filename.endswith('.sid'):
        try:
            sid = open(filename, 'r')

            global client_id
            client_id = sid.readline().strip()

            global client_secret
            client_secret = sid.readline().strip()

            global redirect_uri
            redirect_uri = sid.readline().strip()
        except:
            print ('Problem reading file \'{0}\''.format(filename))
            sys.exit()
    else:
        print ('Invalid file format. File must be of type \'.sid\'')
        sys.exit()

if __name__ == '__main__':
    parse_args(sys.argv)
    main_loop()
