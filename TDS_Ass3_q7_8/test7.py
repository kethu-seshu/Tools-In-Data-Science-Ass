from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
import numpy as np
import os
import uvicorn

# External API URL and token setup for embedding generation
AIPROXY_API_URL = "https://aiproxy.sanand.workers.dev/openai/v1/embeddings"
AIPROXY_TOKEN = os.getenv("AIPROXY_TOKEN", "eyJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6ImtyaXNobmFzYWlrZWVydGhhbi5uYWdhbmRsYUBncmFtZW5lci5jb20ifQ.qR9u0z1VKcT3k5-3D25nJ4hYn1t8nPCW0Zhyl-0Q0kA")

# Initialize FastAPI app
app = FastAPI()

# Enable CORS for all origins and specific methods
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["OPTIONS", "POST"],
    allow_headers=["*"],
)

# Define the request body structure using Pydantic
class SimilarityRequest(BaseModel):
    docs: list[str]
    query: str

@app.post("/similarity")
async def compute_similarity(request_data: SimilarityRequest):
    headers = {"Authorization": f"Bearer {AIPROXY_TOKEN}"}
    
    async with httpx.AsyncClient() as client:
        try:
            # Prepare payload for embedding generation
            payload = {"input": [request_data.query] + request_data.docs, "model": "text-embedding-3-small"}
            response = await client.post(AIPROXY_API_URL, json=payload, headers=headers)
            response.raise_for_status()
            
            data = response.json()
            embeddings = [entry["embedding"] for entry in data["data"]]

            if not embeddings or len(embeddings) != len(request_data.docs) + 1:
                raise HTTPException(status_code=500, detail="Failed to retrieve embeddings.")

            query_embedding = np.array(embeddings[0])  # Query embedding
            doc_embeddings = np.array(embeddings[1:])  # Document embeddings

        except (httpx.RequestError, httpx.HTTPStatusError) as exc:
            raise HTTPException(status_code=500, detail=f"External API request failed: {exc}")

    # Compute cosine similarity between query and documents
    def cosine_similarity(vec1, vec2):
        vec1 = vec1 / np.linalg.norm(vec1)  # Normalize vectors
        vec2 = vec2 / np.linalg.norm(vec2)
        return np.dot(vec1, vec2)

    similarities = [cosine_similarity(query_embedding, doc_embedding) for doc_embedding in doc_embeddings]

    # Rank documents by similarity and return top 3
    ranked_indices = np.argsort(similarities)[::-1][:3]
    matches = [request_data.docs[idx] for idx in ranked_indices]

    return {"matches": matches}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)
