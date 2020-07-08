#!/usr/bin/env python3

import argparse
import os
import sys
import json

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

   parser.add_argument('--no-cache', required=False, action='store_true',
      help='Do not use cached values when fetching posts from Facebook')
   
   parser.add_argument('--dry-run', required=False, action='store_true',
      help='Do a dry run (don\'t actually upload the tracks)')

   args = parser.parse_args()
   return args

def main():
   # Read in the command line args
   args = _parse_args()

   facebook_client = FacebookClient()
   facebook_client.login(LoginType.ENV)
   facebook_group_id = args.facebook_group_id
   
   # Caching logic
   cache_dir = os.path.join(os.getcwd(), 'var', 'cache')
   cache_file = os.path.join(cache_dir, "{}.json".format(facebook_group_id))
   if (args.no_cache) or (not os.path.exists(cache_file)): 
      if (not os.path.exists(cache_dir)):
         os.makedirs(cache_dir)
      print("no-cache specified or cache file does not exist, pulling posts from Facebook group {}".format(facebook_group_id))
      group_posts = facebook_client.query_posts_in_group(facebook_group_id)      
      with open(cache_file, 'w') as cache_fp:
         cache_fp.write(json.dumps(group_posts))
      print("cache file created: {}".format(cache_file))
   else:
      print("using posts from cache file: {}".format(cache_file))
      with open(cache_file, 'r') as cache_fp:
         group_posts = json.load(cache_fp)
 
   shared_links = filter_posts_for_shared_links(group_posts)
   spotify_track_ids = filter_links_for_spotify_track_ids(shared_links)

   spotify_client = SpotifyClient()
   spotify_client.login(LoginType.ENV)
   spotify_playlist_id = args.spotify_playlist_id
   existing_playlist_tracks = spotify_client.get_playlist_tracks(spotify_playlist_id)
 
   tracks_to_add = list(set(spotify_track_ids) - set(existing_playlist_tracks))
   print("Found {} tracks to add to playlist {}:".format(len(tracks_to_add), spotify_playlist_id))

   if not args.dry_run:
      spotify_client.upload_tracks_to_playlist(spotify_playlist_id, tracks_to_add)
   else:
      print("Dry run specified, not adding tracks to playlist. Tracks to add:")
      for track in tracks_to_add:
         print(track)

if __name__ == '__main__':
   main()
