

from sentence_transformers import SentenceTransformer, util
import torch

# Load your fine-tuned model from HuggingFace
MODEL_NAME = "shubham-t/fineTune-sbert"

model = SentenceTransformer(MODEL_NAME)

def semantic_similarity(text1: str, text2: str) -> float:
    emb1 = model.encode(text1, convert_to_tensor=True)
    emb2 = model.encode(text2, convert_to_tensor=True)
    score = util.cos_sim(emb1, emb2).item()
    return round(score, 4)