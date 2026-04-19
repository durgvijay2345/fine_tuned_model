from model import semantic_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Tuned weights
SEMANTIC_WEIGHT = 0.75
LEXICAL_WEIGHT = 0.25

# Tuned threshold
THRESHOLD = 0.75


def lexical_similarity(text1: str, text2: str) -> float:
    """
    Compute TF-IDF cosine similarity
    """
    vectorizer = TfidfVectorizer()

    vectors = vectorizer.fit_transform([text1, text2])

    score = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]

    return round(float(score), 4)


def compute_scores(embed_text1, embed_text2, tfidf_text1, tfidf_text2):
    """
    Use separate text pipelines:
    - embedding text for semantic score
    - tfidf text for lexical score
    """

    sem_score = semantic_similarity(embed_text1, embed_text2)

    lex_score = lexical_similarity(tfidf_text1, tfidf_text2)

    final_score = (
        SEMANTIC_WEIGHT * sem_score +
        LEXICAL_WEIGHT * lex_score
    )

    return {
        "semantic_score": round(sem_score, 4),
        "lexical_score": round(lex_score, 4),
        "final_score": round(final_score, 4)
    }


def classify(score):
    return "Plagiarized" if score >= THRESHOLD else "Not Plagiarized"
