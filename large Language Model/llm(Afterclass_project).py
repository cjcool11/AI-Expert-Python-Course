import requests
from config import HF_API_KEY
from colorama import Fore, Style, init

init(autoreset=True)

DEFAULT_MODEL = "google/pegasus-xsum"

def build_api_url(model_name):
    return f"https://api-inference.huggingface.co/models/{model_name}"

def query(payload, model_name=DEFAULT_MODEL):
    """
    Sends a POST request to the Hugging Face API using the specified model."""

    api_url = build_api_url(model_name)
    headers = {"Authorization": f"bearer {HF_API_KEY}"}
    response = requests.post(api_url, headers=headers, json=payload)
    return response.json()

def summarize_text(text, min_length, max_length, model_name=DEFAULT_MODEL):
    payload = {"inputs": text, "parameters": {"min_length": min_length, "max_length": max_length}}
    print(Fore.BLUE + Style.BRIGHT + f"\n???? Performing AI summarization using model: {model_name}")
    result = query(payload, model_name)

    if isinstance(result, dict) and "error" in result:
        print(Fore.RED + Style.BRIGHT + f"Error: {result['error']}")
    else:
        print(Fore.GREEN + Style.BRIGHT + f"Summary: {result[0]['summary_text']}")

        return result[0]["summary_text"]

if __name__ == "__main__":
    print(Fore.YELLOW + Style.BRIGHT + "???? Hi there! Whats your name? ")
    user_name = input(Fore.CYAN + Style.BRIGHT + "Enter your name: ")
    if not user_name.strip():
        user_name = "User"
    print(Fore.GREEN + Style.BRIGHT + f"Hello, {user_name}! Welcome to the AI Summarization tool.")

    print(Fore.YELLOW + Style.BRIGHT + "???? Please enter the text you want to summarize: ")
    user_text = input("> ").strip()

    if not user_text:
        print(Fore.RED + "No text provided. Exiting...")
    else:
        print(Fore.YELLOW + "\nEnter the model name you want to use for the summarization(e.g: facebook/bart-large-cnn):")
        model_choice = input("> ").strip()
        if not model_choice:
            model_choice = DEFAULT_MODEL

        print(Fore.YELLOW + "\nChoose your summarization style: ")
        print("1. Standard Summary")
        print("2. Enhanced Summary")
        style_choice = input("1 or 2: ").strip()

        if style_choice == "2":
            min_length = 80
            max_length = 200
            print(Fore.BLUE + "enhancing summarization process... ????")

        else:
            min_length = 50
            max_length = 150
            print(Fore.BLUE + "using standard summarization process... ????")

        summary = summarize_text(user_text, min_length, max_length, model_name=model_choice)

        if summary:
            print(Fore.GREEN + f"\n???? AI Summarizer Output for {user_name}: ")
            print(Fore.GREEN + summary)
        else:
            print(Fore.RED + "Summarization failed.")

        