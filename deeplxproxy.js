addEventListener('fetch', event => {
    event.respondWith(handleRequest(event.request));
  })
  
  async function handleRequest(request) {
    if (request.method !== 'POST') {
      return new Response('Method Not Allowed', { status: 405 });
    }
  
    const { text, source_lang, target_lang } = await request.json();
    if (!text || !source_lang ) {
      return new Response('Bad Request', { status: 400 });
    }
  
    // # LibreTranslate api url

    const apiUrl = 'http://127.0.0.1:22381/translate';
    const apiKey = 'your_api_key'; 
  
  
    const payload = {
      q:text,
      source:"auto",
      target:"zh",
      format:"text",
      api_key:"api_key"
    };
  
    const init = {
      method: 'POST',
      headers: {
        // 'Authorization': `Bearer ${apiKey}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(payload)
    };
  
  
  
    try {
      const apiResponse = await fetch(apiUrl, init);
      const apiResponseBody = await apiResponse.json();
  
      if (!apiResponse.ok) {
        return new Response(JSON.stringify(apiResponseBody), { status: apiResponse.status });
      }
  
      return new Response(JSON.stringify( {code:200,data:apiResponseBody.translatedText}), {
        status: 200,
        headers: {
          'Content-Type': 'application/json'
        }
      });
    } catch (error) {
      return new Response('Internal Server Error', { status: 500 });
    }
  }
  