import requests
from config import HF_API_KEY

MODEL_ID = "facebook/bart-large-mnli"
API_URL = f"https://router.huggingface.co/hf-inference/models/{MODEL_ID}"
HEADERS = {"Authorization": f"Bearer {HF_API_KEY}"}
TOPICS = ["Sports", "Technology", "Business", "Politics", "Health"]

def ask_hf(headline: str):
    payload = {"inputs": headline, "parameters": {"candidate_labels": TOPICS}}
    r = requests.post(API_URL, headers=HEADERS, json=payload, timeout=30)
    if not r.ok:
        raise RuntimeError(f"HF error {r.status_code}: {r.text}")
    return r.json()

def best_topic(preds: list):
    best = max(preds, key =lambda x: x["score"])
    return best["label"], best["score"]

def bar(score: float) -> str:
    pct = score * 100
    blocks = int(pct // 10)
    return "█" * blocks + "░" * (10 - blocks)

def show(headline: str, preds: list):
    top_label, top_score = best_topic(preds)
    print("\n" + "=" * 60)
    print("News Topic Classifier")
    print("=" * 60)
    print("Headline: ", headline)
    print(f"Best Topic: {top_label} ({top_score:.2%})")
    print(f"Confidence: {round(top_score*100,1)}% [{bar(top_score)}]")

    print("\nTop 3 guesses: ")
    top3 = sorted(preds, key=lambda x: x["score"], reverse=True)[:3]
    for i, p in enumerate(top3, start=1):
        print(f"{i}. {p['label']:<11} {round(p['score']*100,1)}% [{bar(p['score'])}]")

    print("=" * 60)

def main():
    print("Welcome, type a news headline and I will guess the topic.")
    print("Topics: ", ", ".join(TOPICS))
    print("Type 'exit' to quit.")
    while True:
        headline = input("Headline: ").strip()
        if headline.lower() == "exit":
            break
        if not headline:
            print("Please enter a headline.")
            continue
        try:
            preds = ask_hf(headline)
            if isinstance(preds, list) and preds and "label" in preds[0]:
                show(headline, preds)
            else:
                print("oops, unexpected reply")
        except Exception as e:
            print("Error: ", e)
            print("tip: check HF_API_KEY + internet.\n")

if __name__ == "__main__":
    main()

