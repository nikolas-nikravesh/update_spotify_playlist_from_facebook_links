#!/usr/bin/env python3

def _load_track_ids(track_file):
   with open(track_file) as fp:
      data = fp.read().splitlines()
   return data

def main():
   all_track_ids = _load_track_ids("track_ids.txt")
   existing_track_ids = _load_track_ids("existing_ids.txt")

   print("All tracks length:", len(all_track_ids))
   print("All tracks duplicates removed length:", len(set(all_track_ids)))
   print("Existing tracks length:", len(existing_track_ids))

   tracks_to_be_added = set(all_track_ids) - set(existing_track_ids)
   print("Tracks to be added length:", len(tracks_to_be_added))

   with open("tracks_to_add.txt", 'w') as fp:
      fp.write('\n'.join(tracks_to_be_added))


if __name__ == "__main__":
   main()
