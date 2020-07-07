#!/usr/bin/env python3

import argparse
import os
import sys

sys.path.append(os.path.join(os.getcwd(), "src"))
from my_package.clients import FacebookClient, SpotifyClient, LoginType
from my_package.utils import filter_posts_for_shared_links, filter_links_for_spotify_track_ids

def _parse_args():
   # Args:
   # - The Facebook Group
   # - The Spotify Playlist
   
   parser = argparse.ArgumentParser(description='Get the inputs')

   parser.add_argument('--facebook-group-id', required=True,
      help='The Facebook Group ID in which to pull the tracks from')

   parser.add_argument('--spotify-playlist-id', required=True,
      help='The Sporify Playlist ID to add the tracks to')

   args = parser.parse_args()
   return args


def main():
   # Read in the command line args
   args = _parse_args()
   
   facebook_client = FacebookClient()
   facebook_client.login(LoginType.ENV)
   facebook_group_id = args.facebook_group_id
   group_posts = facebook_client.query_posts_in_group(facebook_group_id)
   
   shared_links = filter_posts_for_shared_links(group_posts)
   spotify_track_ids = filter_links_for_spotify_track_ids(shared_links)

   spotify_client = SpotifyClient()
   spotify_client.login(LoginType.ENV)
   spotify_playlist_id = args.spotify_playlist_id
   existing_playlist_tracks = spotify_client.get_playlist_tracks(spotify_playlist_id)
 
   tracks_to_add = list(set(spotify_track_ids) - set(existing_playlist_tracks))
   spotify_client.upload_tracks_to_playlist(spotify_playlist_id, tracks_to_add)

if __name__ == '__main__':
   main()
