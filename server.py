from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

OLLAMA_API_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "tinyllama:latest"
CONVO_MEMORY = ""

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/static/<path:filename>')
def serve_static_files(filename):
    return send_from_directory(app.static_folder, filename)

@app.route('/query', methods=['POST'])
def query_ollama():
    global CONVO_MEMORY
    data = request.get_json()
    if not data or 'query' not in data:
        return jsonify({"error": "Invalid inputs"}), 400
    
    user_query = data['query']

    payload = {
        "model":MODEL_NAME,
        "prompt":user_query,
        "stream":False
    }

    try:
        response = requests.post(OLLAMA_API_URL, json=payload)
        print("Ollama Response:", response)
        response.raise_for_status()
        ollama_response_json = response.json()
        ollama_response = ollama_response_json.get("response", "No response received")
        
        print(ollama_response_json)
        print(ollama_response)

        return jsonify({"response": ollama_response})
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)    
