from sanic import Sanic
from sanic.response import json
import aiohttp

# Don't forget to install the necessary external Python packages using pip install before getting started!
# python的外部包 记得使用pip install 安装



app = Sanic(__name__)

async def fetch_translation(session, url, payload):
    async with session.post(url, json=payload) as response:
        return await response.json()

@app.route('/translate', methods=['POST'])
async def handle_request(request):
    if request.method != 'POST':
        return json({'error': 'Method Not Allowed'}, status=405)

    data = request.json
    if not data or not data.get('text') or not data.get('source_lang'):
        return json({'error': 'Bad Request'}, status=400)
# # LibreTranslate api url

    api_url = 'http://127.0.0.1:5000/translate'
    api_key = ''

    payload = {
        'q': data['text'],
        'source': 'auto',
        'target': 'zh',
        'format': 'text',
        'api_key': api_key
    }

    async with aiohttp.ClientSession() as session:
        try:
            response = await fetch_translation(session, api_url, payload)
            return json({'code': 200, 'data': response['translatedText']}, status=200)
        except aiohttp.ClientError as e:
            return json({'error': 'Internal Server Error'}, status=500)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7777, debug=True)
