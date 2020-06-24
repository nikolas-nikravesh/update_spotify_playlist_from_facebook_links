#!/usr/bin/env python3

import json
import re

match_track_regex = "(https:\/\/open.spotify.com\/track)\/([a-zA-Z0-9_]*$)"

def _is_spotify_track(link):
   if re.search(match_track_regex, link) is not None:
      return True
   return False

def _get_track_id(link):
   # assume track is in the form 'https://open.spotify.com/track/<some alphanumeric string>'
   match = re.search(match_track_regex, link)
   return match[2]

def main():
   with open("vibes.json") as fp:
      data = json.load(fp)

   track_ids = [_get_track_id(post['link']) for post in data if _is_spotify_track(post['link'])]
   print(track_ids)

   with open('track_ids.txt', 'w') as fp:
      fp.write(("\n".join(track_ids)))
   

if __name__ == "__main__":
   main()
