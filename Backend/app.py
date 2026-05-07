from flask import Flask, request, jsonify
from flask_cors import CORS
from services.groq_service import GroqService

app = Flask(__name__)
# CORS zaroori hai taake frontend ki request block na ho
CORS(app)

# Initialize our custom service
ai_service = GroqService()

@app.route('/api/generate', methods=['POST'])
def generate_document():
    data = request.json
    if not data:
        return jsonify({"success": False, "error": "No data received"}), 400
        
    doc_type = data.get('doc_type')
    details = data.get('details')

    if not details:
        return jsonify({"success": False, "error": "Details are missing"}), 400

    try:
        # Groq API ko call bhejna
        generated_text = ai_service.generate(doc_type, details)
        return jsonify({"success": True, "document": generated_text})
    except Exception as e:
        print("Backend Error:", str(e))
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    print("Starting AI Resume Builder Server...")
    app.run(debug=True, port=5000)