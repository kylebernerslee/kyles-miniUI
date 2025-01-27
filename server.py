from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM

app = Flask(__name__)
CORS(app)

# Define the prompt template
template = """{question}"""

# Initialize the prompt template
prompt = ChatPromptTemplate.from_template(template)

# Initialize the LLM model (Ollama)
llm = OllamaLLM(model="qwen2.5:0.5b-instruct")

# Chain the prompt and the model
chain = prompt | llm

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')  # Serves the static HTML file

@app.route('/query', methods=['POST'])
def query_langchain():
    data = request.get_json()
    if not data or 'query' not in data:
        return jsonify({"error": "Invalid inputs"}), 400

    user_query = data['query']

    try:
        # Process the user query using the prompt + model chain
        response = chain.invoke({"question": user_query})
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
