from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from pytube import YouTube
import json

def fetch_and_save_transcript(url_file):
    with open(url_file, 'r', encoding='utf-8') as file:
        urls = file.readlines()

    # Create or clear the missing.txt file
    open('missing.txt', 'w').close()

    for url in urls:
        try:
            url = url.strip()
            video_id = url.split('watch?v=')[-1]
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            
            # Using pytube to get the video title
            yt = YouTube(url)
            title = yt.title
            
            # Replace characters that are not allowed in filenames
            valid_title = "".join(c for c in title if c not in "\/:*?<>|")

            # Create a dictionary to store both transcript and URL
            data = {
                'url': url,
                'transcript': transcript
            }

            # Save the dictionary as JSON
            with open(f'transcripts/{valid_title}.json', 'w', encoding='utf-8') as json_file:
                json.dump(data, json_file, ensure_ascii=False, indent=4)

        except TranscriptsDisabled:
            # Write the URL to missing.txt if transcripts are disabled
            with open('missing.txt', 'a', encoding='utf-8') as missing_file:
                missing_file.write(url + '\n')
        except Exception as e:
            print(f"Error processing {url}: {e}")

# Example usage
fetch_and_save_transcript('401-NOW.txt')
