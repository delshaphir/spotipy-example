import sys

import spotipy
import spotipy.util as util

SPOTIPY_CLIENT_ID = 'CLIENT_ID'
SPOTIPY_CLIENT_SECRET = 'CLIENT_SECRET'
SPOTIPY_REDIRECT_URI = 'http://google.com'

DEFAULT_LIMIT = 20

class MenuOptionPayload:
    def __init__(self, scope, function):
        self.scope = scope
        self.function = function

def get_token(username, scope):
    return util.prompt_for_user_token(username, scope, SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI)

def top_tracks(sp: spotipy.Spotify):
    print('\nViewing Top Tracks')
    def range_menu():
        range_options = ['Short', 'Medium', 'Long']
        for i, option in enumerate(range_options):
            print('[%i]' % i, option, 'Term')
        choice = 0
        try:
            choice = int(input('> '))
        except:
            print('Invalid input.\n')
            range_menu()
        if choice > len(range_options) - 1:
            print('Invalid input.\n')
            range_menu()
        return range_options[choice].lower() + '_term'
    range_choice = range_menu()
    offset = 0
    print('\nShowing top 20 results...')
    results = sp.current_user_top_tracks(limit=DEFAULT_LIMIT, offset=offset, time_range=range_choice)
    for i, track in enumerate(results['items']):
        print('%i.' % (i + 1 + offset), track['name'], '-', track['artists'][0]['name'])
    while len(input('...')) == 0:
        offset += DEFAULT_LIMIT
        results = sp.current_user_top_tracks(limit=DEFAULT_LIMIT, offset=offset, time_range=range_choice)
        if len(results['items']) == 0:
            print('No more tracks to print.')
            break
        for i, track in enumerate(results['items']):
            print('%i.' % (i + 1 + offset), track['name'], '-', track['artists'][0]['name'])

def top_artists(sp: spotipy.Spotify):
    print('\nViewing Top Artists')
    def range_menu():
        range_options = ['Short', 'Medium', 'Long']
        for i, option in enumerate(range_options):
            print('[%i]' % i, option, 'Term')
        choice = 0
        try:
            choice = int(input('> '))
        except:
            print('Invalid input.\n')
            range_menu()
        if choice > len(range_options) - 1:
            print('Invalid input.\n')
            range_menu()
        return range_options[choice].lower() + '_term'
    range_choice = range_menu()
    offset = 0
    print('\nShowing top %a results...' % DEFAULT_LIMIT)
    results = sp.current_user_top_artists(limit=DEFAULT_LIMIT, offset=offset, time_range=range_choice)
    for i, artist in enumerate(results['items']):
        print('%i.' % (i + 1 + offset), artist['name'])
    while len(input('...')) == 0:
        offset += DEFAULT_LIMIT
        results = sp.current_user_top_artists(limit=DEFAULT_LIMIT, offset=offset, time_range=range_choice)
        if len(results['items']) == 0:
            print('No more artists to print.')
            break
        for i, artist in enumerate(results['items']):
            print('%i.' % (i + 1 + offset), artist['name'])

def playlists(sp: spotipy.Spotify):
    print('\nViewing User Playlists')
    offset = 0
    print('\nShowing top %a results...' % DEFAULT_LIMIT)
    results = sp.current_user_playlists(limit=DEFAULT_LIMIT, offset=offset)
    for i, playlist in enumerate(results['items']):
        print('%i.' % (i + 1 + offset), playlist['name'], '(%a Songs)' % playlist['tracks']['total'])
    while len(input('...')) == 0:
        offset += DEFAULT_LIMIT
        results = sp.current_user_playlists(limit=DEFAULT_LIMIT, offset=offset)
        if len(results['items']) == 0:
            print('No more playlists to print.')
            break
        for i, playlist in enumerate(results['items']):
            print('%i.' % (i + 1 + offset), playlist['name'], '(%a Songs)' % playlist['tracks']['total'])

def search(sp: spotipy.Spotify):
    print('\nSearch Spotify for a(n)...')
    def search_menu():
        search_options = ['Artist', 'Album', 'Track', 'Playlist']
        for i, option in enumerate(search_options):
            print('[%i]' % i, option)
        try:
            choice = int(input('> '))
        except:
            print('Invalid input.\n')
            search_menu()
        if choice > len(search_options) - 1:
            print('Invalid input.\n')
            search_menu()
        return search_options[choice]
    search_type = search_menu().lower()
    offset = 0
    q = input('Query: ')
    results = sp.search(q, limit=DEFAULT_LIMIT, offset=offset, type=search_type)[search_type + 's']
    for i, result in enumerate(results['items']):
        print('%i.' % (i + 1 + offset), result['name'])
    while len(input('...')) == 0:
        offset += DEFAULT_LIMIT
        results = sp.search(q, limit=DEFAULT_LIMIT, offset=offset, type=search_type)[search_type + 's']
        if len(results['items']) == 0:
            print('No more search results to print.')
            break
        for i, result in enumerate(results['items']):
            print('%i.' % (i + 1 + offset), result['name'])

def menu(username):
    menu_options = {
        'See your top tracks': MenuOptionPayload('user-top-read', top_tracks),
        'See your top artists': MenuOptionPayload('user-top-read', top_artists),
        'See your playlists': MenuOptionPayload('playlist-read-collaborative', playlists),
        'Search Spotify': MenuOptionPayload('', search),
        'Exit': MenuOptionPayload('', None),
    }
    print('Welcome,', username)
    for i, option in enumerate(menu_options):
        print('[%i]' % i, option)
    choice = 0
    try:
        choice = int(input('> '))
    except:
        print('Invalid input.\n')
        menu(username)
    payload = menu_options[list(menu_options.keys())[choice]]
    token = get_token(username, payload.scope)
    sp = spotipy.Spotify(auth=token)
    if payload.function == None:
        sys.exit()
    payload.function(sp)
    print()
    menu(username)

def main():
    if len(sys.argv) > 1:
        username = sys.argv[1]
    else:
        print('Usage: %s username' % (sys.argv[0]))
        sys.exit()
    menu(username)

if __name__ == '__main__':
    main()