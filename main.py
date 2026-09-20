import requests
from flask import Flask, render_template, request

app = Flask(__name__)

# Replace with your Hugging Face model repository path
API_URL = "https://api-inference.huggingface.co/models/YOUR_USERNAME/text-summarizer-t5"
# Get a free access token from huggingface.co/settings/tokens
HEADERS = {"Authorization": "Bearer hf_xxxxxxxxxxxxxxxxxxxxxxxx"}

def query_model(payload):
    response = requests.post(API_URL, headers=HEADERS, json=payload)
    return response.json()

@app.route('/', methods=['GET', 'POST'])
def index():
    summary = ""
    original_text = ""
    if request.method == 'POST':
        original_text = request.form.get('content', '')
        if original_text:
            output = query_model({"inputs": original_text})
            # Adjust response key based on output structure
            if isinstance(output, list) and len(output) > 0:
                summary = output[0].get('summary_text', '')
            elif isinstance(output, dict) and 'error' in output:
                summary = f"Model is loading, please try again in a few seconds."
                
    return render_template('index.html', original_text=original_text, summary=summary)

if __name__ == '__main__':
    app.run(debug=True)