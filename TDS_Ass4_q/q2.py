import requests
from bs4 import BeautifulSoup
import json

# IMDb search URL for movies with ratings between 2.0 and 3.0
URL = "https://www.imdb.com/search/title/?user_rating=2,3"

# Define headers to avoid request blocking
HEADERS = {"User-Agent": "Mozilla/5.0"}

# Fetch the page content
response = requests.get(URL, headers=HEADERS)

# Check if request was successful
if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")
    movies = []

    # Loop through movie results
    for item in soup.select(".lister-item-content"):
        title = item.h3.a.text.strip()

        year = item.h3.find("span", class_="lister-item-year")
        year = year.text.strip("()") if year else "Unknown"

        rating_div = item.find("div", class_="inline-block ratings-imdb-rating")
        rating = float(rating_div["data-value"]) if rating_div else None

        movie_id = item.h3.a["href"].split("/")[2]  # Extract IMDb ID from URL

        # Filter movies with rating strictly between 2.0 and 3.0
        if rating and 2.0 <= rating <= 3.0:
            movies.append({
                "id": movie_id,
                "title": title,
                "year": year,
                "rating": rating
            })

        # Stop after collecting 25 valid movies
        if len(movies) >= 25:
            break

    # Convert to JSON format
    movies_json = json.dumps(movies, indent=2)
    
    # Output the JSON data
    print(movies_json)

else:
    print("Failed to fetch data. HTTP Status Code:", response.status_code)
