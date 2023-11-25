from flask import Flask, render_template, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os
import json
import string

# Initialize Flask app
app = Flask(__name__)

limiter = Limiter(app=app, key_func=get_remote_address)


# Function to clean text
def clean_text(text):
    text = text.replace("[Â __Â ]", "****")
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = ' '.join(text.split())
    return text



def format_timestamp(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    return f"{hours}h{minutes}m{seconds}s"  # Updated format


# Search function
def search_transcripts(folder_path, search_term):
    search_term = clean_text(search_term)
    results = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            with open(os.path.join(folder_path, filename), 'r') as file:
                data = json.load(file)
                video_name = filename[:-5]
                video_url = data['url']
                timestamps = []
                texts = []
                urls = []
                for entry in data['transcript']:
                    cleaned_text = clean_text(entry['text'])
                    if search_term in cleaned_text:
                        timestamp = format_timestamp(entry['start'])
                        timestamps.append(timestamp)
                        texts.append(entry['text'])
                        urls.append(f"{video_url}&t={timestamp.replace(':', 'm', 1).replace(':', 's', 1)}")
                if timestamps:
                    results.append([video_name, timestamps, texts, urls])
    return results

@app.route('/')
@limiter.limit("1000 per hour")
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
@limiter.limit("1000 per hour")
def search():
    query = request.form.get('query')
    if not query:
        return render_template('index.html', error="No query provided")
    folder_path = "transcripts/"  # Update this path
    result = search_transcripts(folder_path, query)
    return render_template('index.html', results=result)

if __name__ == '__main__':
    app.run(debug=True)
