#!/usr/bin/env python3.8

from argparse import ArgumentParser, FileType
from utils import *

def main():
    parser = ArgumentParser(description='Check which songs are in your playlists but not liked')
    parser.add_argument('secrets_file', nargs='?', type=FileType('r'), default='secrets.json')

    args = parser.parse_args()
    spotify = connect_to_spotify(args.secrets_file)
    
    current_user = spotify.current_user()
    current_user.pop('images')
    current_user.pop('followers')

    liked_songs_ids = [t['id'] for t in get_all_liked_tracks(spotify, ['id', 'name'])]
    playlists = get_all_playlists(spotify, ['id', 'name', 'owner'], lambda p: p['owner'] == current_user)

    for p in playlists:
        not_liked_songs = get_all_tracks_playlist(spotify, p['id'], ['id', 'name', 'is_local'], lambda t: t['is_local'] and t['id'] not in liked_songs_ids)
        print(('-' * 10) + f"Not Liked Songs in {p['name']}:" + ('-' * 10))
        print('\n'.join(map(lambda s: s['name'], not_liked_songs)))

    

if __name__ == '__main__':
    main()