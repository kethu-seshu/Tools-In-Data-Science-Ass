import requests

def get_newest_delhi_user():
    search_url = "https://api.github.com/search/users"
    params = {
        "q": "location:Dublin followers:>120",
        "sort": "joined",
        "order": "desc",
        "per_page": 1  # Fetch only the newest user
    }
    headers = {"Accept": "application/vnd.github+json"}
    
    response = requests.get(search_url, params=params, headers=headers)
    if response.status_code != 200:
        print("Error fetching user data:", response.json())
        return
    
    users = response.json().get("items", [])
    if not users:
        print("No users found.")
        return
    
    newest_user = users[0]
    username = newest_user["login"]
    user_url = f"https://api.github.com/users/{username}"
    
    user_response = requests.get(user_url, headers=headers)
    if user_response.status_code != 200:
        print("Error fetching user details:", user_response.json())
        return
    
    user_data = user_response.json()
    print(f"Newest user: {username}")
    print(f"GitHub profile: {user_data['html_url']}")
    print(f"Account created at: {user_data['created_at']}")

if __name__ == "__main__":
    get_newest_delhi_user()