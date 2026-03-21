from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
# Permitir que tu frontend en GitHub Pages haga fetch
CORS(app, resources={r"/chat": {"origins": "https://imankd06.github.io"}})

OPENROUTER_KEY = os.getenv("OPENROUTER_KEY")
SYSTEM_PROMPT = os.getenv("SYSTEM_PROMPT")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True)
    messages = data.get("messages", [])

    prompt_forzado = {"role": "system", "content": SYSTEM_PROMPT}
    mensaje_entero = [prompt_forzado] + messages

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {OPENROUTER_KEY}"
            },
            json={"model": "openrouter/free", "messages": mensaje_entero}
        )
        r = response.json()

        if "choices" in r and len(r["choices"]) > 0:
            asistente_mensaje = r["choices"][0]["message"]["content"]
        else:
            asistente_mensaje = f"Error del modelo: {r}"

        return jsonify({"response": asistente_mensaje})

    except Exception as e:
        return jsonify({"response": f"Error en el servidor: {str(e)}"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # toma el puerto de Render
    app.run(host="0.0.0.0", port=port)
