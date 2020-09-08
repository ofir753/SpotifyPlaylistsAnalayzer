# Spotify Playlist Analayzer

Tools to find some stuff about your playlists.

## Tools
* `songs_not_in_liked.py` - Check which songs are in your playlists but not liked

## Installation
```pip install -r pip_requirements.txt```

## Usage
Create an app in https://developer.spotify.com/dashboard/applications \
You can use any valid url for the redirect uri "http://example.com" for example \
Create `secrets.json` file \
```json
{
	"spotify-api-clientid": "",
	"spotify-api-secret": "",
	"spotify-api-redirect_uri": ""
}
```
