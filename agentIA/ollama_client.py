import httpx

async def generate_text(prompt: str):
    async with httpx.AsyncClient(
        timeout=120
    ) as client:

        response = await client.post(
            "http://ollama:11434/api/generate",
            json={
                "model": "qwen2.5:1.5b",
                "prompt": prompt,
                "stream": False,
                "options": {
                    "num_predict": 20,
                    "temperature": 0.4,
                    "top_k": 20,
                    "num_ctx": 512
                }
            }
        )

        data = response.json()

        return data["response"].strip()