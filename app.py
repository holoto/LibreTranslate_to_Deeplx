import requests
from flask import Flask, request, jsonify

# Don't forget to install the necessary external Python packages using pip install before getting started!
# python的外部包 记得使用pip install 安装






app = Flask(__name__)

@app.route('/translate', methods=['POST'])
def handle_request():
    if request.method != 'POST':
        return jsonify({'error': 'Method Not Allowed'}), 405

    data = request.get_json()
    if not data or not data.get('text') or not data.get('source_lang'):
        return jsonify({'error': 'Bad Request'}), 400
# LibreTranslate api url
    api_url = 'http://127.0.0.1:5000/translate' 
    api_key = ''

    payload = {
        'q': data['text'],
        'source': 'auto',
        'target': 'zh',
        'format': 'text',
        'api_key': api_key
    }

    try:
        response = requests.post(api_url, json=payload)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return jsonify({'error': 'Internal Server Error'}), 500

    return jsonify({'code': 200, 'data': response.json()['translatedText']}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9999, debug=True)


