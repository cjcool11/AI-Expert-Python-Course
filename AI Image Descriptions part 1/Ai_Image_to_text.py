from config import HF_API_KEY
import requests, base64, os, re
from PIL import Image
from colorama import init, Fore, Style

init(autoreset=True)

ROUTER_URL = "https://router.huggingface.co/v1/chat/completions"
HEADERS = {"Authorization": f"Bearer {HF_API_KEY}", "Content-Type": "application/json"}

# ONLY ONE GUARANTEED WORKING VISION MODEL
VISION_MODELS = [
    "moonshotai/Kimi-K2.6:novita",
]

# TEXT MODELS (safe)
TEXT_MODELS = [
    "Qwen/Qwen2.5-7B-Instruct:together",
    "Qwen/Qwen2.5-14B-Instruct:together",
    "Qwen/Qwen2.5-32B-Instruct:together",
    "mistralai/Mistral-7B-Instruct-v0.3:together",
    "mistralai/Mixtral-8x7B-Instruct-v0.1:together",
]

def _data_url(path: str) -> str:
    with open(path, "rb") as f:
        return "data:image/jpeg;base64," + base64.b64encode(f.read()).decode("utf-8")

def query_hf_api(payload: dict):
    try:
        r = requests.post(ROUTER_URL, headers=HEADERS, json=payload, timeout=40)
    except Exception as e:
        return None, f"Request failed: {e}"

    if r.status_code != 200:
        try:
            j = r.json()
            msg = j.get("error", {}).get("message") or str(j)
        except Exception:
            msg = r.text or "Unknown error"
        return None, f"Status {r.status_code}: {msg}"

    try:
        return r.json(), None
    except Exception:
        return None, "Non‑JSON response."

def extract_text(data) -> str:
    try:
        return data["choices"][0]["message"]["content"].strip()
    except:
        return ""

def _run_models(models, messages, max_tokens=160, temperature=0.3):
    last_err = None
    for model in models:
        print(f"{Fore.MAGENTA}Trying model: {model}")

        data, err = query_hf_api({
            "model": model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature
        })

        if err:
            print(f"{Fore.RED}Model error: {err}")
            last_err = err
            continue

        out = extract_text(data)
        if out:
            print(f"{Fore.GREEN}Model succeeded: {model}")
            return out, None

        last_err = "Empty response."

    return None, last_err or "All models failed."

def _words(text: str):
    return re.findall(r"\S+", (text or "").strip())

def _exact_n_words(text: str, n: int) -> str:
    return " ".join(_words(text)[:n])

def _ensure_sentence_end(text: str) -> str:
    t = text.strip()
    if t and t[-1] not in ".!?":
        t += "."
    return t

def get_basic_caption(image_path: str) -> str:
    print(f"{Fore.YELLOW}Generating basic caption...")
    msgs = [{
        "role": "user",
        "content": [
            {"type": "text", "text": "Write one complete sentence describing this image."},
            {"type": "image_url", "image_url": {"url": _data_url(image_path)}},
        ],
    }]
    cap, err = _run_models(VISION_MODELS, msgs, max_tokens=90, temperature=0.2)
    return cap if cap else f"[error] {err}"

def print_menu():
    print(f"""{Style.BRIGHT}{Fore.GREEN}
=============================== MENU ==============================
select output type:
1. Caption (5 words)
2. Description (30 words)
3. Summary (50 words)
4. Exit 
===================================================================
""")

def generate_text(prompt: str, max_new_tokens: int = 220) -> str:
    msgs = [{"role": "user", "content": prompt}]
    out, err = _run_models(TEXT_MODELS, msgs, max_tokens=max_new_tokens, temperature=0.4)
    if err:
        raise Exception(err)
    return out

def generate_exact_sentence(prompt: str, n_words: int, max_new_tokens: int, tries: int = 6) -> str:
    for _ in range(tries):
        out = generate_text(prompt, max_new_tokens=max_new_tokens)
        words = _words(out)
        if len(words) == n_words:
            return _ensure_sentence_end(out)
    raise Exception(f"Failed to produce exactly {n_words} words after {tries} tries.")

def main():
    image_path = input(f"{Fore.BLUE}Enter the path to the image file: {Style.RESET_ALL}")
    if not os.path.exists(image_path):
        print(f"{Fore.RED}File does not exist.")
        return

    try:
        Image.open(image_path)
    except Exception as e:
        print(f"{Fore.RED}Failed to open image: {e}")

    basic_caption = get_basic_caption(image_path)
    print(f"{Fore.YELLOW}Basic caption: {Fore.CYAN}{basic_caption}")

    while True:
        print_menu()
        choice = input(f"{Fore.BLUE}Enter your choice (1-4): {Style.RESET_ALL}").strip()

        if basic_caption.startswith("[error]") and choice in {"1", "2", "3"}:
            basic_caption = get_basic_caption(image_path)
            print(f"{Fore.YELLOW}Basic caption: {Fore.CYAN}{basic_caption}\n")

        if choice == "1":
            if basic_caption.startswith("[error]"):
                print(f"{Fore.RED}Caption (5 words): {Fore.CYAN}{basic_caption}\n")
            else:
                out = _ensure_sentence_end(_exact_n_words(basic_caption, 5))
                print(f"{Fore.GREEN}Caption (5 words): {Fore.CYAN}{out}\n")

        elif choice == "2":
            if basic_caption.startswith("[error]"):
                print(f"{Fore.RED}Failed to generate description.")
                continue
            prompt = (
                "Rewrite as EXACTLY 30 words. One complete sentence. End with a period.\n\nText: "
                + basic_caption
            )
            try:
                out = generate_exact_sentence(prompt, 30, max_new_tokens=220, tries=6)
                print(f"{Fore.GREEN}Description (30 words): {Fore.YELLOW}{out}\n")
            except Exception as e:
                print(f"{Fore.RED}Error: {e}\n")

        elif choice == "3":
            if basic_caption.startswith("[error]"):
                print(f"{Fore.RED}Failed to generate summary.")
                continue
            prompt = (
                "Write EXACTLY 50 words. One complete sentence. End with a period.\n\nImage seed: "
                + basic_caption
            )
            try:
                out = generate_exact_sentence(prompt, 50, max_new_tokens=280, tries=7)
                print(f"{Fore.GREEN}Summary (50 words): {Fore.YELLOW}{out}\n")
            except Exception as e:
                print(f"{Fore.RED}Error: {e}\n")

        elif choice == "4":
            print(f"{Fore.BLUE}Goodbye!")
            break

        else:
            print(f"{Fore.RED}Invalid choice.\n")

if __name__ == "__main__":
    main()
