import httpx

async def get(url):
    async with httpx.AsyncClient(timeout=None) as client:
        resp = await client.get(
            url,
        )
        return resp
