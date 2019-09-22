# Spotipy Example

## Overview
[Spotipy](https://spotipy.readthedocs.io/en/latest/) is a handy Python library that makes it even easier to use the [Spotify API](https://developer.spotify.com/documentation/web-api/). This is a small example of how it can be used to bring some Spotify client functionality to the command line.

## Getting Started with Spotipy
If you have pip, you can install Spotipy from the command-line with the following.
```
pip install spotipy
```
If you somehow don't have pip, [follow these instructions](https://pip.pypa.io/en/stable/installing/) to get it.

## How This Works
Behind-the-scenes, Spotipy is making HTTP requests to the Spotify Web API, which returns results in JSON format. Luckily, Spotipiy provides some abstraction for this process, so we can just use the `spotipy.Spotify` object to call methods as we need them.

Methods called in this example include:
- `current_user_top_tracks`: Returns the top tracks for the current user
- `current_user_top_artists`: Returns the top artists for the current user
- `current_user_playlists`: Returns the current user's playlists
- `search`: Returns the results of a search on Spotify for a given query

### Tokens & Authorization
The Spotify object is initialized with a `token`, which can be generated thanks to the handy dandy `spotify.util` library. All you need is the following:
1. Username of a Spotify account
2. Scope
3. Client ID
4. Client Secret
5. Redirect URI

Passing these five (5) pieces of information into `spotipy.util.prompt_for_user_token` will prompt the user (of the username given) to log in and grant permission for your app to do what it does. The specific permissions asked for are determined by the **scope**, which is just a string you can pass along so Spotify knows what to ask the user. [Here is a full list of possible scopes](https://developer.spotify.com/documentation/general/guides/scopes/).

The **Client ID** and **Client Secret** must be generated from the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/login). Just log in and follow the instructions to create your app and generate your Client ID and Secret.

Also in the Dashboard, you should whitelist a **redirect URI**, which is simply a URI to which Spotify will redirect your user after asking for permission on behalf of your app. This example uses "http://google.com".

## Reading the Data

When you call a method from the Spotify object, the results return as JSON objects, which Python so conveniently reads as a dictionary. Then, just use the keys to get the information you want. For example, printing the name of a user's first top artist looks like so:
```
results = spotify.current_user_top_artists()
print(results['items'][0]['name'])
```
Here, we're using the `items` key to get the list of items (in this case, JSON objects representing artists) from `results`. Then, we're getting the artist object at index 0, and using the `name` key to find that artist's name. Voilà!