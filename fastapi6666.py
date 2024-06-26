from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import httpx
import asyncio
import hypercorn.config
import hypercorn.asyncio


app = FastAPI()

async def fetch_translation(client, url, payload):
    response = await client.post(url, json=payload)
    response.raise_for_status()  # Raise exception for non-2xx status codes
    return response.json()

@app.post("/translate")
async def translate_text(request: Request):
    try:
        data = await request.json()
    except JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON data")
    
    if not data or not data.get('text') or not data.get('source_lang'):
        raise HTTPException(status_code=400, detail="Bad Request")

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
            return JSONResponse({"data": response["translatedText"], "code": 200})
        except httpx.RequestError as e:
            return JSONResponse({'error': 'Internal Server Error'}, 500)

if __name__ == "__main__":
    config = hypercorn.config.Config()
    config.bind = ["0.0.0.0:6666"]
    asyncio.run(hypercorn.asyncio.serve(app, config))



