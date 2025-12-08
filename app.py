# app.py

from flask import Flask, render_template, request, jsonify
from processing_incoming import answer_question

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")  # looks in templates/index.html


@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("question", "").strip()

    if not question:
        return jsonify({"error": "Question is required"}), 400

    try:
        answer = answer_question(question)
        return jsonify({"answer": answer})
    except Exception as e:
        print("Error in /ask:", e)
        return jsonify({"error": "Something went wrong on the server."}), 500


if __name__ == "__main__":
    # host='0.0.0.0' if you want to expose on network
    app.run(debug=True)
