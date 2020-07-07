import re

MATCH_TRACK_REGEX = "(https:\/\/open.spotify.com\/track)\/([a-zA-Z0-9_]*$)"

# returns whether the link is a spotify track
def is_spotify_track(link):
   if re.search(MATCH_TRACK_REGEX, link) is not None:
      return True
   return False

# gets a track ID from a Spotify link
def get_track_id(link):
   # assume track is in the form 'https://open.spotify.com/track/<some alphanumeric string>'
   match = re.search(MATCH_TRACK_REGEX, link)
   return match[2]

# filter the posts, and return a list of all the links that were shared on a post
def filter_posts_for_shared_links(posts):
    print("Filtering posts for shared links")
    links = []
    for entry in posts:
        try:
            attachments = entry["attachments"]["data"]
            for attachment in attachments:
                track_link = attachment["unshimmed_url"]
                print("Found shared link:", track_link)
                links.append(track_link)
        except:
            entry_utf_8 = {k.encode('utf8'): v.encode('utf8') for k, v in entry.items()}
            #print("Entry does not have track ID:", entry_utf_8)
    
    return links

# filters a list of links, returning a list of spotify track IDs from the list
def filter_links_for_spotify_track_ids(links):
    print("Filtering links for Spotify track IDs")
    spotify_track_ids = [get_track_id(link) for link in links if is_spotify_track(link)]
    return spotify_track_ids
