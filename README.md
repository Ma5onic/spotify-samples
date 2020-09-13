# spotify-samples

API that checks what you are playing on Spotify and finds samples used in that song by scraping WhoSampled.com

## Currently Playing 
**Endpoint:** /api/currently-playing/samples <br>
**You get:** A list of samples from a track you are currently playing on Spotify

**Successful Response:**
```json
{
  "original_track": {
    "artists": [
      "Warren G",
      "Nate Dogg"
    ],
    "name": "Regulate"
  },
  "samples": [
    {
      "track_artist": "Michael McDonald",
      "track_name": "I Keep Forgettin'",
      "track_url": "https://open.spotify.com/track/5GvWrvLIqoHroq7YvO260M"
    },
    {
      "track_artist": "Bob James",
      "track_name": "Sign of the Times",
      "track_url": "https://open.spotify.com/track/4d2VOdbKfPt7wA7S5Hzn6x"
    },
    {
      "track_artist": "Parliament",
      "track_name": "Mothership Connection (Star Child)",
      "track_url": "https://open.spotify.com/track/7rLAPi81R7qlVqgXfykdEL"
    }
  ],
  "whosampled_url": "https://www.whosampled.com/Warren-G/Regulate/"
}