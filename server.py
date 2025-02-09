from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from langchain.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama

app = Flask(__name__)
CORS(app)

# Define the prompt template
template = """Respond sarcastically to this query: {question}"""

# Initialize the prompt template
prompt = ChatPromptTemplate.from_template(template)

# Initialize the LLM model (Ollama)
llm = ChatOllama(model="tinydolphin", streaming=False)

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')  # Serves the static HTML file

@app.route('/query', methods=['POST'])
def query_langchain():
    data = request.get_json()

    if not data or 'query' not in data or 'uniqueId' not in data:
        return jsonify({"error": "Invalid inputs, missing 'query' or 'uniqueId'"}), 400

    user_query = data['query']
    user_id = data['uniqueId']

    # Log user_id for debugging purposes
    print(f"Received query from user: {user_id}")

    try:
        # Format the prompt with the user query
        formatted_prompt = prompt.format(question=user_query)
        print(formatted_prompt)

        # Get the response from the model (LLM)
        response = llm.invoke(formatted_prompt)

        # Convert the response to a JSON-serializable format
        response_content = response.content

        # Return the response as JSON
        return jsonify({"response": response_content})

    except Exception as e:
        # Log the error for debugging purposes
        print(f"Error processing query: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
