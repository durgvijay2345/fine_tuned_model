from flask import Flask, request, jsonify
from flask_cors import CORS
from PyPDF2 import PdfReader
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer, util
import re
import numpy as np


# Flask App Setup


app = Flask(__name__)
CORS(app)


# Load Model Once (important for performance)


model = SentenceTransformer("all-MiniLM-L6-v2")


# Config


SEMANTIC_WEIGHT = 0.75
LEXICAL_WEIGHT = 0.25
THRESHOLD = 0.75


# Preprocessing Functions


def basic_clean(text):
    """
    Basic cleaning used by both pipelines
    """
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def preprocess_for_embedding(text):
    """
    Keep stopwords for embeddings
    because transformers need context.
    """
    text = basic_clean(text)
    return text


def preprocess_for_tfidf(text):
    """
    Remove punctuation + stopwords
    for lexical similarity.
    """
    text = basic_clean(text)

    # remove punctuation
    text = re.sub(r"[^\w\s]", "", text)

    words = text.split()
    words = [w for w in words if w not in ENGLISH_STOP_WORDS]

    return " ".join(words).strip()


# PDF Extraction


def extract_text_from_pdf(file):
    reader = PdfReader(file)
    text = ""

    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + " "

    return text.strip()


# Similarity Functions


def semantic_similarity(text1, text2):
    emb1 = model.encode(text1, convert_to_tensor=True)
    emb2 = model.encode(text2, convert_to_tensor=True)

    score = util.cos_sim(emb1, emb2).item()
    return round(float(score), 4)


def lexical_similarity(text1, text2):
    vectorizer = TfidfVectorizer()

    vectors = vectorizer.fit_transform([text1, text2])

    score = cosine_similarity(vectors[0], vectors[1])[0][0]

    return round(float(score), 4)


def compute_scores(raw_text1, raw_text2):
    """
    Use different preprocessing for
    embeddings and TF-IDF
    """

    # ---------- Embedding Pipeline ----------
    embed_text1 = preprocess_for_embedding(raw_text1)
    embed_text2 = preprocess_for_embedding(raw_text2)

    # ---------- TF-IDF Pipeline ----------
    tfidf_text1 = preprocess_for_tfidf(raw_text1)
    tfidf_text2 = preprocess_for_tfidf(raw_text2)

    # ---------- Scores ----------
    semantic_score = semantic_similarity(embed_text1, embed_text2)
    lexical_score = lexical_similarity(tfidf_text1, tfidf_text2)

    final_score = (
        SEMANTIC_WEIGHT * semantic_score +
        LEXICAL_WEIGHT * lexical_score
    )

    final_score = round(float(final_score), 4)

    return {
        "semantic_score": semantic_score,
        "lexical_score": lexical_score,
        "final_score": final_score
    }


# Classification


def classify(score):
    if score >= THRESHOLD:
        return "Plagiarized"
    return "Not Plagiarized"


# Routes


@app.route("/")
def home():
    return jsonify({
        "message": "AI Plagiarism Detection API Running"
    })



# Text Input Route


@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()

        text1 = data.get("text1", "")
        text2 = data.get("text2", "")

        if not text1 or not text2:
            return jsonify({
                "error": "Both text1 and text2 are required"
            }), 400

        scores = compute_scores(text1, text2)

        result = classify(scores["final_score"])

        return jsonify({
            "semantic_similarity": scores["semantic_score"],
            "lexical_similarity": scores["lexical_score"],
            "final_similarity": scores["final_score"],
            "classification": result
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500



# PDF Input Route


@app.route("/predict-file", methods=["POST"])
def predict_file():
    try:
        file1 = request.files.get("file1")
        file2 = request.files.get("file2")

        if not file1 or not file2:
            return jsonify({
                "error": "Both files are required"
            }), 400

        text1 = extract_text_from_pdf(file1)
        text2 = extract_text_from_pdf(file2)

        if not text1.strip() or not text2.strip():
            return jsonify({
                "error": "Could not extract text from PDFs"
            }), 400

        scores = compute_scores(text1, text2)

        result = classify(scores["final_score"])

        return jsonify({
            "semantic_similarity": scores["semantic_score"],
            "lexical_similarity": scores["lexical_score"],
            "final_similarity": scores["final_score"],
            "classification": result
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500




if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
