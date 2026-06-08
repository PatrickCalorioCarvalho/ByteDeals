import httpx

async def fetch_html(url: str):

    headers = {
        "User-Agent": (
            "Mozilla/5.0 "
            "(Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 "
            "(KHTML, like Gecko) "
            "Chrome/125.0.0.0 Safari/537.36"
        )
    }

    async with httpx.AsyncClient(
        follow_redirects=True,
        timeout=30
    ) as client:

        response = await client.get(
            url,
            headers=headers
        )

        return response.text
