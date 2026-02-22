from model import semantic_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def lexical_similarity(text1, text2):
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([text1, text2])
    score = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
    return round(score, 4)


def compute_scores(text1, text2):
    sem_score = semantic_similarity(text1, text2)
    lex_score = lexical_similarity(text1, text2)

    final_score = (0.75 * sem_score) + (0.25 * lex_score)

    return {
        "semantic_score": round(sem_score, 4),
        "lexical_score": round(lex_score, 4),
        "final_score": round(final_score, 4)
    }


def classify(score, threshold=0.75):
    return "Plagiarized" if score >= threshold else "Not Plagiarized"