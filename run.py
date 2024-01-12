from youtube_client import YoutubeClient
import os
def run():
    youtube = YoutubeClient('./creds/client_secret.json')

    playlists = youtube.get_playlist()


    for index, playlist in enumerate(playlists):
        print(f"{index} - {playlist.title}")
    choice = int(input("Choose a playlist: "))
    chosen_playlist = playlists[choice]
    print(f"You chose {chosen_playlist.title}")

    videos = youtube.get_video_from_playlist(chosen_playlist.id)
    print(f"Attempting to add {len(videos)} videos to spotify")

    for video in videos:
        print(f"Adding {video.artist} - {video.track}")
        spotify_id = youtube.get_spotify_id(video.artist, video.track)
        if spotify_id:
            print(f"Adding {video.artist} - {video.track} to spotify")
            youtube.add_song_to_spotify(spotify_id)
        else:
            print(f"Could not find {video.artist} - {video.track} in spotify")




if __name__ == "__main__":
    run()