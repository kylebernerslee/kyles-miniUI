import os
from flask import Flask, request, jsonify, send_from_directory, Response
from flask_cors import CORS
from langchain.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama

app = Flask(__name__)
CORS(app)

OLLAMA_MODEL = "dolphin3"
LOGS_DIRECTORY = './logs'
os.makedirs(LOGS_DIRECTORY, exist_ok=True)


# Define the prompt
system_prompt = "You are Dolphin The Golphin, referenced to as AI, an AI User assistant that is really helpful, but also always a sarcastic ass. Play your role as good as you can. This is how the conversation has gone so far, your answers are labeled AI: and the User's querys and interactions are labeled USER:"


# Initialize the LLM model (Ollama) with streaming enabled
llm = ChatOllama(model=OLLAMA_MODEL, streaming=True)

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')  # Serves the static HTML file

def log_to_file(unique_id, content):
    """Helper function to append to the .md file or create it if it doesn't exist"""
    file_path = os.path.join(LOGS_DIRECTORY, f"{unique_id}.md")

    # If the file doesn't exist, we'll create it with the initial prompt
    if not os.path.exists(file_path):
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(f"{content}\n\n")
    else:
        with open(file_path, 'a', encoding='utf-8') as f:
            f.write(f"{content}\n\n")

def read_log_for_user(user_id):
    """
    Reads the log file for the given user_id and returns the content as a string.

    :param user_id: Unique identifier for the user (corresponds to the filename).
    :return: The content of the log file as a string, or a message if the file does not exist.
    """
    # Construct the file path based on the user_id
    file_path = os.path.join(LOGS_DIRECTORY, f"{user_id}.md")

    # Check if the file exists
    if not os.path.exists(file_path):
        return f"No log file found for user {user_id}"

    # Read the content of the file
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return content
    except Exception as e:
        return f"Error reading the log file: {str(e)}"

def generate_streamed_response(user_query, user_id):
    print(user_query)
    try:
        # Stream the response from the model
        conversation_answer = ""
        for chunk in llm.stream(user_query):
            conversation_answer += chunk.content
            yield chunk.content  # Yield the chunk as a response stream
    except Exception as e:
        yield f"Error: {str(e)}"  # Stream error message if there's an issue

    log_to_file(user_id, f"AI:\n{conversation_answer}")


@app.route('/query', methods=['POST'])
def query_langchain():
    data = request.get_json()

    # Check for required fields in the request data
    if not data or 'query' not in data or 'uniqueId' not in data:
        return jsonify({"error": "Invalid inputs, missing 'query' or 'uniqueId'"}), 400

    user_query = data['query']
    user_id = data['uniqueId']

    history = read_log_for_user(user_id)

    # Log the unique ID and query for debugging
    print(f"Received query from user (ID: {user_id}): {user_query}")

    final_query = f"This is your role in this conversation:\n{system_prompt}\n\nThis is the context of our conversation so far:\n{history}\n\nAnd this is the new query from USER:\n{user_query}"

    # Log the initial query to the file
    log_to_file(user_id, f"USER:\n{user_query}")

    # Stream the response back to the client
    return Response(generate_streamed_response(final_query, user_id), content_type='text/plain; charset=utf-8')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
