#!/usr/bin/env python3

import argparse
import os
import sys
import json
import logging

sys.path.append(os.path.join(os.getcwd(), "src"))
from my_package.clients import FacebookClient, SpotifyClient, LoginType
from my_package.utils import filter_posts_for_shared_links, filter_links_for_spotify_track_ids

log_level_map = {
   "WARNING": logging.WARNING,
   "INFO": logging.INFO,
   "DEBUG": logging.DEBUG
}

def _parse_args():
   parser = argparse.ArgumentParser(description='Get the inputs')

   parser.add_argument('--facebook-group-id', required=True,
      help='The Facebook Group ID in which to pull the tracks from')

   parser.add_argument('--spotify-playlist-id', required=True,
      help='The Spotify Playlist ID to add the tracks to')

   parser.add_argument('--no-cache', required=False, action='store_true',
      help='Do not use cached values when fetching posts from Facebook')
   
   parser.add_argument('--dry-run', required=False, action='store_true',
      help='Do a dry run (don\'t actually upload the tracks)')
   
   parser.add_argument('--log-level', required=False, default="DEBUG",
      help='Specify the log level for the application log. Valid choices are WARNING, INFO, DEBUG')

   args = parser.parse_args()
   return args

def _get_facebook_group_posts(args, facebook_client):
   logging.info("Pulling Facebook posts from group %s", args.facebook_group_id)
   # Caching logic
   cache_dir = os.path.join(os.getcwd(), 'var', 'cache')
   cache_file = os.path.join(cache_dir, "{}.json".format(args.facebook_group_id))
   if (args.no_cache) or (not os.path.exists(cache_file)): 
      os.makedirs(cache_dir, exist_ok=True)
      logging.debug("No-cache specified or cache file does not exist, pulling posts from Facebook group {}".format(args.facebook_group_id))

      group_posts = facebook_client.query_posts_in_group(args.facebook_group_id)      

      with open(cache_file, 'w') as cache_fp:
         cache_fp.write(json.dumps(group_posts))
      logging.debug("cache file created: {}".format(cache_file))
   else:
      logging.debug("Using posts from cache file: {}".format(cache_file))
      with open(cache_file, 'r') as cache_fp:
         group_posts = json.load(cache_fp)
 
   return group_posts


def _get_tracks_to_add(args, spotify_client, spotify_track_ids):
   logging.info("Determining tracks that need to be added to playlist %s", args.spotify_playlist_id)

   spotify_playlist_id = args.spotify_playlist_id
   existing_playlist_tracks = spotify_client.get_playlist_tracks(spotify_playlist_id)
 
   tracks_to_add = list(set(spotify_track_ids) - set(existing_playlist_tracks))
   print("Found {} tracks to add to playlist {}:".format(len(tracks_to_add), spotify_playlist_id))
   return tracks_to_add

def _upload_spotify_tracks(args, spotify_client, tracks_to_add):
   logging.info("Uploading tracks to Spotify playlist %s", args.spotify_playlist_id)
   if not args.dry_run:
      if len(tracks_to_add) <= 0:
         print("No new tracks to add.")
         sys.exit(0)
      response = input("WARNING: You are about to add {} tracks to spotify playlist {}. ".format(len(tracks_to_add), args.spotify_playlist_id) + 
         "Are you sure? (y/n)\n--> ")
      if response.lower() != "y":
         print("Aborting upload.")
         sys.exit(1)
      spotify_client.upload_tracks_to_playlist(args.spotify_playlist_id, tracks_to_add)
   else:
      print("Dry run specified, not adding tracks to playlist.")

def _initialize_logger(log_level):
   if log_level not in log_level_map:
      print('Log level "{}" is not a valid option.'.format(log_level))
      sys.exit(1)
   
   var_dir = os.path.join(os.getcwd(), 'var')
   os.makedirs(var_dir, exist_ok=True)
   log_file = os.path.join(var_dir, 'application.log')

   print("Log file:", log_file)

   logging.basicConfig(filename=log_file, format='%(asctime)s [%(levelname)s] %(message)s', level=log_level_map[log_level])
   logging.info('Logger initialized')

def main():
   args = _parse_args()
   _initialize_logger(args.log_level)

   login_type = LoginType.ENV

   facebook_client = FacebookClient()
   facebook_client.login(login_type)

   spotify_client = SpotifyClient()
   spotify_client.login(login_type)

   print("Getting group posts from Facebook")
   group_posts = _get_facebook_group_posts(args, facebook_client) 

   print("Filtering posts for Spotify links")
   shared_links = filter_posts_for_shared_links(group_posts)
   spotify_track_ids = filter_links_for_spotify_track_ids(shared_links)

   print("Determining tracks to add to Spotify")
   tracks_to_add = _get_tracks_to_add(args, spotify_client, spotify_track_ids)
   
   print("Uploading tracks to spotify")
   _upload_spotify_tracks(args, spotify_client, tracks_to_add)

   print("Upload complete.")

if __name__ == '__main__':
   main()
