from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.requests import Request
import aiohttp
import asyncio
import hypercorn.asyncio
import hypercorn.config

app = Starlette()

async def fetch_translation(session, url, payload):
    async with session.post(url, json=payload) as response:
        response.raise_for_status()  # Raise exception for non-2xx status codes
        return await response.json()

@app.route("/translate", methods=["POST"])
async def translate_text(request: Request):
    data = await request.json()
    if not data or not data.get('text') or not data.get('source_lang'):
        return JSONResponse({'error': 'Bad Request'}, 400)

    api_url = "http://127.0.0.1:5000/translate"
    api_key = ""

    payload = {
        "q": data['text'],
        "source": "auto",
        "target": "zh",
        "format": "text",
        "api_key": api_key,
    }

    async with aiohttp.ClientSession() as session:
        try:
            response = await fetch_translation(session, api_url, payload)
            return JSONResponse({"data": response["translatedText"], "code": 200})
        except aiohttp.ClientError as e:
            return JSONResponse({'error': 'Internal Server Error'}, 500)

if __name__ == "__main__":
    config = hypercorn.config.Config()
    config.bind = ["0.0.0.0:11111"]
    asyncio.run(hypercorn.asyncio.serve(app, config))
