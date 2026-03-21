from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/chat": {"origins": os.getenv("ALLOWED_ORIGIN")}})

OPENROUTER_KEY = os.getenv("OPENROUTER_KEY")
SYSTEM_PROMPT = os.getenv("SYSTEM_PROMPT")

# Ruta para servir tu portafolio
@app.route("/")
def home():
    return render_template("index.html")

# Ruta del chatbot
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
    app.run(host="0.0.0.0", port=5000)
