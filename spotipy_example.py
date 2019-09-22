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
    """Returns an authentication token, given a username and scope."""
    return util.prompt_for_user_token(username, scope, SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI)

def new_menu(options):
    """
    Creates a new menu with the given set of options and returns 
    the user-chosen index. Retries until the user chooses a vaild index
    (a parseable integer in the bounds of the given array).
    """

    def invalid_input():
        print('Invalid input.\n')
        new_menu(options)
    for i, option in enumerate(options):
        print('[%i]' % i, option)
    choice = 0
    try:
        choice = int(input('> '))
    except:
        invalid_input()
    if choice > len(options) - 1:
        invalid_input()
    return choice

def top_tracks(sp: spotipy.Spotify):
    """View the current user's top tracks."""

    print('\nViewing Top Tracks')
    range_options = {
        'Short Term': 'short_term',
        'Medium Term': 'medium_term',
        'Long Term': 'long_term',
    }
    choice = new_menu(range_options.keys())
    range_choice = range_options[list(range_options.keys())[choice]]
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
    """View the current user's top artists. """

    print('\nViewing Top Artists')
    range_options = {
        'Short Term': 'short_term',
        'Medium Term': 'medium_term',
        'Long Term': 'long_term',
    }
    choice = new_menu(range_options.keys())
    range_choice = range_options[list(range_options.keys())[choice]]
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
    """View the current user's playlists."""

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
    """View the Spotify search results of a given query."""

    print('\nSearch Spotify for a(n)...')
    search_options = ['Artist', 'Album', 'Track', 'Playlist']
    choice = new_menu(search_options)
    search_type = search_options[choice].lower()
    search_type_key = search_type + 's'
    offset = 0
    q = input('Query: ')
    results = sp.search(q, limit=DEFAULT_LIMIT, offset=offset, type=search_type)[search_type_key]
    for i, result in enumerate(results['items']):
        if search_type == 'album' or search_type == 'track':
            output = result['name'] + ' - ' + result['artists'][0]['name']
        else:
            output = result['name']
        print('%i.' % (i + 1 + offset), output)
    while len(input('...')) == 0:
        offset += DEFAULT_LIMIT
        results = sp.search(q, limit=DEFAULT_LIMIT, offset=offset, type=search_type)[search_type_key]
        if len(results['items']) == 0:
            print('No more search results to print.')
            break
        for i, result in enumerate(results['items']):
            print('%i.' % (i + 1 + offset), result['name'])

def menu(username):
    """Runs the main menu."""

    menu_options = {
        'See your top tracks': MenuOptionPayload('user-top-read', top_tracks),
        'See your top artists': MenuOptionPayload('user-top-read', top_artists),
        'See your playlists': MenuOptionPayload('playlist-read-collaborative', playlists),
        'Search Spotify': MenuOptionPayload('', search),
        'Exit': MenuOptionPayload('', None),
    }
    choice = new_menu(menu_options.keys())
    payload = menu_options[list(menu_options.keys())[choice]]
    if payload.function == None:
        sys.exit()
    token = get_token(username, payload.scope)
    sp = spotipy.Spotify(auth=token)
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