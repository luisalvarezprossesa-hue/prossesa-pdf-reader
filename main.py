from flask import Flask, request, jsonify
import anthropic
import base64

app = Flask(__name__)
client = anthropic.Anthropic()

@app.route('/leer-pdf', methods=['POST'])
def leer_pdf():
    data = request.json
    pdf_base64 = data.get('pdf_base64')
    lista_trabajadores = data.get('lista_trabajadores', '')
    
    prompt = f"""Analiza esta lista de asistencia y extrae los trabajadores presentes.

Lista maestra de trabajadores (nombre y gafete):
{lista_trabajadores}

Instrucciones:
1. Lee los nombres y gafetes del PDF
2. Compara con la lista maestra usando similitud de nombre O gafete
3. Devuelve SOLO JSON con este formato exacto, sin explicaciones:
[{{"gafete": "12345", "nombre": "NOMBRE COMPLETO", "dia": "10"}}]

El campo "dia" es el día del mes que aparece en la fecha del documento."""

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
                    "text": prompt
                }
            ]
        }]
    )
    
    return jsonify({"resultado": message.content[0].text})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
