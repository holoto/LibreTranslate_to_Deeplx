from fastapi import FastAPI, HTTPException
import requests
import uvicorn

# Don't forget to install the necessary external Python packages using pip install before getting started!
# python的外部包 记得使用pip install 安装



app = FastAPI()

@app.post("/translate/")
async def translate_text(text: str, source_lang: str):
    if not text or not source_lang:
        raise HTTPException(status_code=400, detail="Missing required parameters")
# # LibreTranslate api url

    api_url = "http://127.0.0.1:5000/translate"
    api_key = ""

    payload = {
        "q": text,
        "source": "auto",
        "target": "zh",
        "format": "text",
        "api_key": api_key,
    }

    try:
        response = requests.post(api_url, json=payload)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail="Internal server error")

    return {"translated_text": response.json()["translatedText"]}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=6666)








