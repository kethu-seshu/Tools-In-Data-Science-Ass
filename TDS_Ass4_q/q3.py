from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import requests
from bs4 import BeautifulSoup

app = FastAPI()

# Enable CORS to allow access from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

WIKI_BASE_URL = "https://en.wikipedia.org/wiki/"

@app.get("/api/outline")
async def get_country_outline(country: str = Query(..., title="Country Name")):
    """
    Fetch the Wikipedia page of a country, extract all headings (H1-H6), 
    and return a Markdown-formatted outline.
    """
    url = WIKI_BASE_URL + country.replace(" ", "_")
    response = requests.get(url)

    if response.status_code != 200:
        return {"error": "Country not found or Wikipedia page unavailable"}

    soup = BeautifulSoup(response.text, "html.parser")
    headings = soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])

    markdown_outline = "## Contents\n\n"
    for heading in headings:
        level = int(heading.name[1])  # Extract the number from h1-h6
        markdown_outline += f"{'#' * level} {heading.text.strip()}\n\n"

    return {"country": country, "outline": markdown_outline.strip()}


# uvicorn q3:app --port 8001 --reload