from sanic import Sanic, request, json

import asyncio
import hypercorn.asyncio
import hypercorn.config


import httpx

app = Sanic(__name__)

async def fetch_translation(client, url, payload):
    response = await client.post(url, json=payload)
    response.raise_for_status()
    return response.json()

@app.post("/translate")
async def translate_text(request):
    data = request.json
    if not data or not data.get('text') or not data.get('source_lang'):
        return json({'error': 'Bad Request'}, 400)

    api_url = "http://127.0.0.1:5000/translate"
    api_key = ""

    payload = {
        "q": data['text'],
        "source": "auto",
        "target": "zh",
        "format": "text",
        "api_key": api_key,
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await fetch_translation(client, api_url, payload)
            return json({"data": response["translatedText"],"code":200})
        except httpx.RequestError as e:
            return json({'error': 'Internal Server Error'}, 500)

if __name__ == "__main__":
    config = hypercorn.config.Config()
    config.bind = ["0.0.0.0:7777"]
    asyncio.run(hypercorn.asyncio.serve(app, config))
