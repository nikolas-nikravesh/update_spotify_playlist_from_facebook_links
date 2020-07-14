# update_spotify_playlist_from_facebook_links

## Purpose

I am a member of a Facebook group dedicated to sharing good music that we come across. This music is shared in the form of links (i.e. spotify links, youtube links, etc). 

We also have a spotify playlist that a member of the group tries to keep updated when people post new spotify links in the group.

The problem with this is that it can become tedious to constantly attend to the facebook page and update the spotify playlist, especially when posts are made daily, meaning that they will accumulate quickly. 

I decided to play around with the Facebook Graph API and the Spotify developer API to see if I could query the group in which I am a part of, extract all the links that are shared, and then automatically update the spotify playlist with the songs that are 
not already present.

## User Guide

### Prerequisites

Sadly, in order to get this working completely, I need to register my app with both Facebook and Spotify. I am too lazy to do that right now. Because of this, getting this to work requires to do a couple things:

#### Get authentication tokens
In order for this to work, you need authentication tokens for both the Facebook and Spotify APIs. As mentioned, since this app is not registerd, this is the best way I know how to obtain temporary credentials:

* Sign up for a [Facebook Developers account](https://developers.facebook.com/). You will need this to get an authentication token to query the API
* Get an authentication token from your developer account. The easiest way I found to do this was to just create a new app. 
    * You will need permission `groups_access_member_info` added to your profile. See [examples](https://developers.facebook.com/docs/groups-api/common-uses/)
* An authentication token with access to your Spotify playlist. See [this example](https://developer.spotify.com/console/post-playlist-tracks/) to help you get started. You will need `playlist-modify-public` and `playlist-modify-private` permissions

#### Other necessary prerequisites

* Ensure you are an Admin of the Facebook page which will be used. (not sure if this is strictly required, but nice to have)
* Get the Facebook group ID. This can be found in the url in the form `https://www.facebook.com/groups/<group id>`
* Get the Spotify playlist ID. This can be found by going to your playlist, clicking the (...) object near the title of the playlist, then clicking "Share" --> "Copy Spotify URI". You will only need the string of random characters from this (i.e. `spotify:playlist:<random string of characters>`)

### Package dependencies
For your convenience, a Dockerfile is included in this project. You can run the application in a Docker container built from this Dockerfile if you don't want to worry about installing dependencies or modifying your normal environment. 

Otherwise, the dependencies are:
* python3 
* requests for python3 (`pip3 install requests`)

### Run the program

#### Checkout this package

```
git clone https://github.com/nikolasn97/update_spotify_playlist_from_facebook_links.git
```

#### Set authentication tokens as environment variables
First, set the authentication tokens as environment variables
```
export FACEBOOK_ACCESS_TOKEN=<your facebook authentication token>
export SPOTIFY_ACCESS_TOKEN=<your spotify authentication token>
```

#### Run the program
Run the program by executing the following from the package root  
```
./bin/run.py --facebook-group-id <facebook group id> --spotify-playlist-id <spotify playlist id> 
```
This will take all the posts in the specified Facebook group with links to Spotify songs shared, and put them in the Spotify playlist specified by the playlist ID.

For more information on this application, you can run 
```
./bin/run.py --help
```
To see a complete list of command line options

## Further Reading

You can read more about using the Facebook Graph API [here](https://developers.facebook.com/docs/graph-api/)

You can read more about using the Spotify API [here](https://developer.spotify.com/)
