#!/usr/bin/env python3.8

import spotipy
import json
from os import environ
from spotipy.oauth2 import SpotifyOAuth
from argparse import ArgumentParser, FileType
import datetime
from itertools import chain

SPOTIFY_PLAYLIST_SCOPE = 'playlist-read-collaborative playlist-read-private user-library-read'
SECRETS_CLIENT_ID = 'spotify-api-clientid'
SECRETS_SECRET_ID = 'spotify-api-secret'
SECRETS_REDIRECT_URI = 'spotify-api-redirect_uri'
CACHE_PATH = 'cache_file'

DEFAULT_FILTER_LAMBDA = lambda a: True

def get_all_tracks_playlist(spotify, playlist_id, keys_to_return=None, filter_lambda=DEFAULT_FILTER_LAMBDA):
    spotify_result = spotify.user_playlist('spotify', playlist_id)

    return get_all(spotify, spotify_result['tracks'], 'track', keys_to_return=keys_to_return, filter_lambda=filter_lambda)

def get_all_liked_tracks(spotify, keys_to_return=None, filter_lambda=DEFAULT_FILTER_LAMBDA):
    spotify_result = spotify.current_user_saved_tracks()

    return get_all(spotify, spotify_result, 'track', keys_to_return=keys_to_return, filter_lambda=filter_lambda)

def get_all_playlists(spotify, keys_to_return=None, filter_lambda=DEFAULT_FILTER_LAMBDA):
    spotify_result = spotify.current_user_playlists()

    return get_all(spotify, spotify_result, keys_to_return=keys_to_return, filter_lambda=filter_lambda)

def filter_items(items, main_key, keys_to_return, filter_lambda):
    if main_key != None:
        items = map(lambda item: item[main_key], items)

    if keys_to_return != None:
        items = map(lambda item: {k: item[k] for k in keys_to_return}, items)

    items = filter(filter_lambda, items)
    
    return items


def get_all(spotify, spotify_result, main_key=None, keys_to_return=None, filter_lambda=DEFAULT_FILTER_LAMBDA):
    items = filter_items(spotify_result['items'], main_key, keys_to_return, filter_lambda)

    while spotify_result['next']:
        spotify_result = spotify.next(spotify_result)
        items = chain(items, filter_items(spotify_result['items'], main_key, keys_to_return, filter_lambda))

    return items

def connect_to_spotify(secrets_file_stream):
    secrets = json.load(secrets_file_stream)
    spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=SPOTIFY_PLAYLIST_SCOPE,
                        client_id=secrets[SECRETS_CLIENT_ID],
                        client_secret=secrets[SECRETS_SECRET_ID],
                        redirect_uri=secrets[SECRETS_REDIRECT_URI],
                        cache_path=CACHE_PATH))

    return spotify