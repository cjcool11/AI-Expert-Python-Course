import requests

def get_random_user():
    """Generate a random user from the user generator API."""
    url = "https://randomuser.me"
    response = requests.get(url)

    if response.status_code == 200:
        print(f"Full JSON Response: {response.json()}")
        user_data = response.json()
        return f"{user_data['name']} - {user_data['birthday']}"
    else:
        return "Failed to retrieve user."
    
def main():
    print("Welcome to the Random User Generator! ")

    while True:
        user_input = input("Press Enter to get a new user, or type 'q'/'exit to quit: ").strip().lower()

        if user_input in ("q", "exit"):
            print("Goodbye!")
            break

        user = get_random_user()
        print(user)

if __name__ == "__main__":
    main()