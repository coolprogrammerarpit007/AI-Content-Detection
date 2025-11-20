from transformers import pipeline
from app.ml.categories import CATEGORIES

# Load model once (heavy)
classifier = pipeline(
    "zero-shot-classification",
    model="typeform/distilbert-base-uncased-mnli",
    device=-1
)

def classify_text(text: str) -> str:
    result = classifier(
        sequences=text,
        candidate_labels=CATEGORIES,
        multi_label=False
    )

    best_category = result["labels"][0]
    return best_category.lower()
