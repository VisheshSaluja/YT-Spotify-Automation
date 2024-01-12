import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import yt_dlp as youtube_dl  # Import yt_dlp as youtube_dl

class Playlist(object):
    def __init__(self, id, title):
        self.id = id
        self.title = title

class Song(object):
    def __init__(self, artist, track):
        self.artist = artist
        self.track = track

class YoutubeClient(object):
    def __init__(self, credentials_location):
        scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        api_service_name = "youtube"
        api_version = "v3"

        # Ensure the credentials file is not hardcoded but read from a secure place
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            credentials_location, scopes)
        credentials = flow.run_local_server(port=8080)

        youtube = googleapiclient.discovery.build(
            api_service_name, api_version, credentials=credentials)
        
        self.youtube_client = youtube

    def get_playlist(self):
        request = self.youtube_client.playlists().list(
            part="id, snippet",
            maxResults=50,
            mine=True
        )
        response = request.execute()

        playlists = [Playlist(item['id'], item['snippet']['title']) for item in response["items"]]
        return playlists

    def get_video_from_playlist(self, playlist_id):
        songs = []
        request = self.youtube_client.playlistItems().list(
            playlistId=playlist_id,
            part="id, snippet",
        )
        response = request.execute()

        for item in response["items"]:
            video_id = item["snippet"]["resourceId"]["videoId"]
            arist, track = self.get_artist_and_track_from_video(video_id)

            print(f"Extracted - Artist: {arist}, Track: {track}")

            if arist and track:
                songs.append(Song(arist, track))
        
        return songs

    def get_artist_and_track_from_video(self, video_id):
        youtube_url = f"https://www.youtube.com/watch?v={video_id}"

        ydl_opts = {
            'quiet': True,
            'nocheckcertificate': True,
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            video = ydl.extract_info(youtube_url, download=False)

        title = video.get('title')
        if title:
            # Custom parsing logic based on your video title format
            parts = title.split(" - ")
            if len(parts) >= 2:
                return parts[0].strip(), parts[1].strip()
        return None, None

