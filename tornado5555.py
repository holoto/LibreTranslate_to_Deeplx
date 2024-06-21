import json
import tornado.web
import tornado.httpserver
import tornado.ioloop
import httpx


class TranslationHandler(tornado.web.RequestHandler):
    async def post(self):
        try:
            data = json.loads(self.request.body)
            if not data or not data.get('text') or not data.get('source_lang'):
                raise tornado.web.HTTPError(400, reason="Bad Request")

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
                response = await client.post(api_url, json=payload)
                response.raise_for_status()
                # response_data = await  response.json()
                response_data =   response.json()
                self.write({"data": response_data["translatedText"], "code": 200})
        except (json.JSONDecodeError, tornado.web.HTTPError) as e:
            self.write_error(status_code=500, reason=str(e))
        except httpx.RequestError as e:
            self.write_error(status_code=500, reason="Internal Server Error")

if __name__ == "__main__":
    app = tornado.web.Application([
        (r"/translate", TranslationHandler),
    ])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(5555)
    tornado.ioloop.IOLoop.current().start()
