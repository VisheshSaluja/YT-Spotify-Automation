import os
import requests
import urllib.parse
import webbrowser

# Use environment variables for sensitive data
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")  # This should match the redirect URI registered in Spotify Developer Dashboard
SCOPE = "user-library-modify"  # Adjust the scope as needed

def get_authorization_url():
    params = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": SCOPE,
        "show_dialog": "true"
    }
    return f"https://accounts.spotify.com/authorize?{urllib.parse.urlencode(params)}"

def get_api_token(code):
    url = "https://accounts.spotify.com/api/token"
    payload = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }
    response = requests.post(url, data=payload)
    return response.json().get("access_token")

def main():
    # Step 1: Direct the user to the authorization URL
    auth_url = get_authorization_url()
    print("Please go to this URL and authorize access:")
    print(auth_url)

    # Step 2: User inputs the authorization code from the redirect URL
    auth_code = input("Enter the code from the URL here: ")

    # Step 3: Exchange the code for an access token
    api_token = get_api_token(auth_code)
    print(f"Your access token is: {api_token}")

    # Initialize Spotify client with the access token
    spotify_client = SpotifyClient(api_token)

class SpotifyClient(object):
    def __init__(self, api_token):
        self.api_token = api_token

    def search_song(self, artist, track):
        query = urllib.parse.quote_plus(f"{artist} {track}")
        url = f"https://api.spotify.com/v1/search?q={query}&type=track"
        response = requests.get(
            url, 
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_token}"
            }
        )

        response_json = response.json()


        results = response_json["tracks"]["items"]

        if results:
            return results[0]['id']
        else:
            raise Exception(f"No results found for {artist} - {track}")

    def add_song_to_spotify(self, song_id):
        url = f"https://api.spotify.com/v1/me/tracks"
        response = requests.put(
            url,
            json={
                "ids": [song_id]
            },
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_token}"
                
            }
        )

        return response.ok

if __name__ == "__main__":
    main()

