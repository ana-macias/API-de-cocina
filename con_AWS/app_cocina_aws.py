from flask import Flask, request, jsonify
import groq
from groq import Groq
import os 
from bdaws_cocina import crear_tabla_aws 
from bdaws_cocina import (  
    guardar_consulta_aws as guardar_consulta,
    obtener_historial_aws as obtener_historial
) # Importamos desde el nuevo archivo

app = Flask(__name__)
app.config['DEBUG'] = True

def es_de_cocina(pregunta: str) -> bool:
    """Usa el modelo para clasificar el tema de la pregunta"""
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    
    clasificacion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "Eres un clasificador de temas. Responde SOLO con 'True' o 'False' si la pregunta está relacionada con COCINA (recetas, ingredientes, técnicas culinarias, gastronomía, nutrición)."
            },
            {
                "role": "user",
                "content": f"¿Esta pregunta es sobre cocina?: '{pregunta}'"
            }
        ],
        model="llama3-70b-8192",
        temperature=0,
        max_tokens=10
    )
    
    return "true" in clasificacion.choices[0].message.content.lower()


def modelo(pregunta):
    client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
    )    
    chat_completion = client.chat.completions.create(
        messages=[
            {
            "role": "system",
            "content": "Eres un chef experto. Responde preguntas sobre cocina de forma detallada. Si la pregunta no es de cocina, di amablemente que solo puedes hablar de temas culinarios."
            },
    
             {
            "role": "user",
            "content": pregunta,
            }
    ],
    model="llama3-70b-8192",
    stream=False,
    )

    respuesta = chat_completion.choices[0].message.content
    guardar_consulta(pregunta, respuesta)
    return respuesta


@app.route('/', methods = ['GET'])
def main():
    return 'API de conexion al LLM de cocina. Bienvenido al maravilloso mundo de la cocina. Pregunta lo que quieras'

@app.route('/pront/<string:pregunta>', methods = ['GET'])
def pront(pregunta):
    try:
        if not es_de_cocina(pregunta):
            return jsonify({
                "error": "Lo siento, solo respondo preguntas sobre cocina",
                "sugerencia": "Pregunta sobre recetas, ingredientes o técnicas culinarias"
            }), 400
        
        respuesta = modelo(pregunta)
    
        return jsonify({"respuesta": respuesta})
    
    except Exception as e:
        return jsonify({"error": f"Error procesando la pregunta: {str(e)}"}), 500
    
@app.route('/historial', methods = ['GET'])
def historial():
    registros = obtener_historial()
    return jsonify({"historial": registros})
    
if __name__ == '__main__':
    crear_tabla_aws()
    app.run() 