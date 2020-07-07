import os
import enum

from my_package.http import get, post

class LoginType(enum.Enum): 
    EXPLICIT = 1
    ENV = 2
    
class FacebookClient:
    def __init__(self):
        print("FacebookClient initialized")
        self.access_token = None
        self.message_limit = 100 # max number of messages to retrieve per request

    # In order to access the Facebook API, you need an authentication token
    # To do this, you can either do an explicit login and enter your Facebook credentials,
    # or specify the access token string as an environment variable
    def login(self, login_type):
        print("Getting credentials for the Facebook Client with login type:", login_type)
        if login_type == LoginType.EXPLICIT:
            # TODO: explicit login
            raise Exception("Explicit Login not implemented")
        elif login_type == LoginType.ENV:
            self.access_token = os.environ.get('FACEBOOK_ACCESS_TOKEN', None)
            if self.access_token is None:
                raise Exception("FACEBOOK_ACCESS_TOKEN environment variable not set. Please set it or change your login method")
        else:
            raise Exception("Apparently there exists an unhandled LoginType:", login_type)
    
    # Queries the facebook group specified by the group ID and returns all the posts
    # from this page
    def query_posts_in_group(self, facebook_group_id):
        print("Getting all posts from Facebook group with ID: ", facebook_group_id)
        url = "https://graph.facebook.com/v7.0/{0}/feed?fields=attachments%7Bunshimmed_url%7D%2Cmessage&limit={1}&access_token={2}".format(facebook_group_id, self.message_limit, self.access_token)
        posts = []
        while url is not None:
            print("Retrieving {} entries from group {}".format(self.message_limit, facebook_group_id))
            _, page_data = get(url) 
            
            # there may be more than self.message_limit posts, so continue with the next set of 
            # entires until there are no more 
            if page_data.get('data') is not None:
                posts.extend(page_data['data'])
            
            if page_data.get("paging", None) is None:
                break    
            url = page_data["paging"].get("next", None) 
            print("Paging to next set of entries")
        
        print("All posts retrieved from group.")
        return posts


class SpotifyClient:
    def __init__(self):
        print("SpotifyClient initialized")
        self.access_token = None
        self.headers = None
    
    def login(self, login_type):
        print("Getting credentials for the Spotify Client with login type:", login_type)
        if login_type == LoginType.EXPLICIT:
            # TODO: explicit login
            raise Exception("Explicit Login not implemented")
        elif login_type == LoginType.ENV:
            self.access_token = os.environ.get('SPOTIFY_ACCESS_TOKEN', None)
            if self.access_token is None:
                raise Exception("SPOTIFY_ACCESS_TOKEN environment variable not set. Please set it or change your login method")
        else:
            raise Exception("Apparently there exists an unhandled LoginType:", login_type)

        self.headers = {
            "Authorization" : "Bearer {}".format(self.access_token),
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
    
    def upload_tracks_to_playlist(self, spotify_playlist_id, tracks):
        if len(tracks) == 0:
            print("Nothing to upload.")
            return
        
        print("Uploading {} track(s) to Spotify".format(len(tracks)))
        for track_id in tracks:
            print("Uploading track ID {}".format(track_id))
            url="https://api.spotify.com/v1/playlists/{}/tracks?uris=spotify%3Atrack%3A{}".format(spotify_playlist_id, track_id)
            response = post(url, headers=self.headers)

    def get_playlist_tracks(self, spotify_playlist_id):
        print("Getting all tracks from Spotify playlist with ID: ", spotify_playlist_id)
        tracks = []
        url = "https://api.spotify.com/v1/playlists/{}/tracks".format(spotify_playlist_id)

        while url is not None:
            print("Retrieving playlist tracks...")
            _, data = get(url, headers=self.headers)
            url = data.get("next", None)
            track_ids = self._get_track_from_data(data['items'])
            tracks.extend(track_ids)
        
        return tracks
    
    # TODO: Fix this somehow
    def _get_track_from_data(self, items):
        track_ids = []
        for item in items:
            try:
                track = item["track"]
                if track['type'] == 'track':
                    track_id = track['id']
                    track_ids.append(track_id)
            except:
                print("Could not get track ID")
        
        return track_ids