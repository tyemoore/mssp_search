from pytube import Playlist

def save_playlist_urls(playlist_url, n):
    try:
        playlist = Playlist(playlist_url)
        # Fetch playlist videos
        playlist._video_regex = None  # This is to circumvent a known issue in pytube
        videos = playlist.video_urls

        # Save first n URLs to a file
        with open('401-NOW.txt', 'w') as file:
            for video_url in videos[:n]:
                file.write(video_url + '\n')
        
        print(f"Saved URLs of the first {n} videos from the playlist to URLS.txt")
    except Exception as e:
        print("An error occurred:", e)

if __name__ == "__main__":
    playlist_url = "https://www.youtube.com/playlist?list=PL-zWbO9RZaSNL0oLkXQPAEvxJ_JzrA00i"
    number_of_videos = 154  # You can change this number to save a different amount of videos
    save_playlist_urls(playlist_url, number_of_videos)
