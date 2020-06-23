# update_spotify_playlist_from_facebook_links
Playing around with the Facebook API for developers

## Purpose

I am a member of a Facebook group dedicated to sharing good music that we come across. 
This music is shared in the form of links (i.e. spotify links, youtube links, etc). 

We also have a spotify playlist that a member of the group tries to keep updated when 
people post new spotify links in the group.

The problem with this is that it can become tedious to constantly attend to the facebook page 
and update the spotify playlist, especially when posts are made daily, meaning that they will accumulate quickly. 

I decided to play around with the Facebook Graph API to see if I could query the group in which I am a part of,
extract all the links that are shared, and then automatically update the spotify playlist with the songs that are 
not already present.

#### Note from Developer

Currently, I have the Facebook Graph API requests functioning, but I have not yet added the Spotify side of this

## User Guide

### Get data from Facebook

#### Prerequisites

In order to get this working in your own account, you will need to set the following things up

* Sign up for a [Facebook Developers account](https://developers.facebook.com/). You will need this to get an authentication token 
  to query the API
* Get an authentication token from your developer account. The easiest way I found to do this was to just create a new app. 
    * You will need permission `groups_access_member_info` added to your profile. See [examples](https://developers.facebook.com/docs/groups-api/common-uses/)
* Ensure you are an Admin of the Facebook page which will be used
* Install `jq`, a command line json parsing tool

#### Retrieving the data
In order to get posts from a facebook page, use the following query. You will need to get the group ID from the Facebook link (go to the group 
in a browser and grab the ID from the url) and your authentication token with the proper permissions

To see posts for a group
```
export ACCESS_TOKEN=<Your access token here>
export GROUP_ID=<Your facebook group ID here>
export MESSAGE_LIMIT=<Number of messages you wish to view>
export OUT_FILE=<file to send the output to>

./get_group_posts $ACCESS_TOKEN $GROUP_ID $MESSAGE_LIMIT $OUT_FILE
```

An example output will look something like this
```
cat data.json | jq
{
  "data": [
    {
      "message": "This one's a classic",
      "id": "XXXXXXXXXXXX",
      "attachments": {
        "data": [
          {
            "unshimmed_url": "https://open.spotify.com/track/44CZRkOxv7UItaAUmh8PgN"
          }
        ]
      }
    },
    {
      "message": "Check out this song!",
      "id": "XXXXXXXXXXXX",
      "attachments": {
        "data": [
          {
            "unshimmed_url": "https://open.spotify.com/track/50R5Or6xMtvELGYfGUbVz4"
          }
        ]
      }
    },
	.
	.
	.
	.
	.
```


To parse the output for only posts that include shared links
```
export IN_FILE=<name of input file with the JSON data of posts>
export OUT_FILE=<file to save the parsed output>

./parse_posts_for_links $IN_FILE $OUT_FILE
```

The parsed data will look something like this
```
cat links.json| jq
{
  "message": "This one's a classic",
  "link": "https://open.spotify.com/track/44CZRkOxv7UItaAUmh8PgN"
}
{
  "message": "Check out this song!",
  "link": "https://open.spotify.com/track/50R5Or6xMtvELGYfGUbVz4"
}
```

Now you have a concise list for all the shared links on your facebook page!

### Add songs to a Spotify playlist

#### Prerequisites

Similarly to the Facebook API, some information is needed in order to use the spotify API
* The playlist ID. This can be found by going to your playlist, clicking the (...) looking object near the title of the playlist,
    then clicking "Share" --> "Copy Spotify URI". You will only need the string of random characters from this
* The [song URI](https://developer.spotify.com/documentation/web-api/#spotify-uris-and-ids) for the song you'd like to add
* An authentication token with access to your playlist. See [this example](https://developer.spotify.com/console/post-playlist-tracks/) to help you get started

#### Uploading a song to your Spotify playlist

Run the script
```
export PLAYLIST_ID=<Your Spotify playlist ID>
export TRACK_ID=<The Spotify song URI>
export AUTH_TOKEN=<Your spotify Auth Token>
./add_song_to_spotify_playlist $PLAYLIST_ID $TRACK_ID $AUTH_TOKEN
```

If all goes well, you will see a return value of a snapshot ID with your query info
```
{
  "snapshot_id" : "TAOELTI2MTkxYmExOTM5ZDNlZjQ3OGJjYENAMWHQMTEzYTcwNjNmMWY4ZA=="
}
```

Now, check out your Spotify playlist to see the songs updated in your account!

## Further Reading

You can read more about using the Facebook Graph API [here](https://developers.facebook.com/docs/graph-api/)
You can read more about using the Spotify API [here](https://developer.spotify.com/)
