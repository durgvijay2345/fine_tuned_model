from flask import Flask, request, jsonify
from flask_cors import CORS
from PyPDF2 import PdfReader
from ensemble import compute_scores, classify

app = Flask(__name__)
CORS(app)


def extract_text_from_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted
    return text


@app.route("/")
def home():
    return jsonify({"message": "Plagiarism Detection API Running 🚀"})


@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        text1 = data.get("text1", "")
        text2 = data.get("text2", "")

        if not text1 or not text2:
            return jsonify({"error": "Both text1 and text2 are required"}), 400

        scores = compute_scores(text1, text2)
        result = classify(scores["final_score"])

        return jsonify({
            "semantic_similarity": scores["semantic_score"],
            "lexical_similarity": scores["lexical_score"],
            "final_similarity": scores["final_score"],
            "classification": result
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/predict-file", methods=["POST"])
def predict_file():
    try:
        file1 = request.files.get("file1")
        file2 = request.files.get("file2")

        if not file1 or not file2:
            return jsonify({"error": "Both files are required"}), 400

        text1 = extract_text_from_pdf(file1)
        text2 = extract_text_from_pdf(file2)

        if not text1.strip() or not text2.strip():
            return jsonify({"error": "Could not extract text from PDF"}), 400

        scores = compute_scores(text1, text2)
        result = classify(scores["final_score"])

        return jsonify({
            "semantic_similarity": scores["semantic_score"],
            "lexical_similarity": scores["lexical_score"],
            "final_similarity": scores["final_score"],
            "classification": result
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)