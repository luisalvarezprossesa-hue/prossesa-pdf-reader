from flask import Flask, request, jsonify
import anthropic
import base64

app = Flask(__name__)
client = anthropic.Anthropic()

@app.route('/leer-pdf', methods=['POST'])
def leer_pdf():
    data = request.json
    pdf_base64 = data.get('pdf_base64')
    
    message = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": [
                {
                    "type": "document",
                    "source": {
                        "type": "base64",
                        "media_type": "application/pdf",
                        "data": pdf_base64
                    }
                },
                {
                    "type": "text",
                    "text": "Extrae todos los nombres, números de gafete y área de esta lista de asistencia. Devuelve solo JSON: [{\"nombre\":\"...\",\"gafete\":\"...\",\"area\":\"...\"}]"
                }
            ]
        }]
    )
    
    return jsonify({"resultado": message.content[0].text})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
