
import httpx

def analyze_sentiment():
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": "Seshu dummy_api_key",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "Analyze the sentiment of the following text and classify it as GOOD, BAD, or NEUTRAL."},
            {"role": "user", "content": "zNVajSclZVC t3Pn IrZTz U2X oQy8DZ8EcP  y   ThxQfp5"}
        ]
    }
    
    response = httpx.post(url, json=payload, headers=headers)
    response.raise_for_status()
    
    data = response.json()
    print(data)

if __name__ == "__main__":
    analyze_sentiment()
