Utilities
=========

* How to get a refresh token from Google?

- Get a OAuth2 Client here: https://code.google.com/apis/console/
- Follow instructions here: https://developers.google.com/accounts/docs/OAuth2WebServer#offline
- Once you have an auth code, you must exchange it for a refresh token
- The refresh token is another curl away, using the same URL, but setting the code (newly acquired), client\_id, clien\_secret, redirect\_uri and grant\_type=authorization\_code
- Once you have the refresh token, setup a crontab at every 15 or 30 minutes to keep a fresh token for use on server at all times
- It's another curl, but with client\_id, clien\_secret, refresh\_token (the one you just got) and grant\_type=refresh\_token
- Output to home directory or some local repository for future use
