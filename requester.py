import httpx

URL = "http://localhost:9000"

async def post(data: bytes) -> str:
    print(f"Enviando requisicao para {URL}...")

    async with httpx.AsyncClient() as client:
        resp = await client.post(URL, content=data)
        resp.raise_for_status()
        return resp.text