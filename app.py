import os
import requests
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify, session
from flask_session import Session

load_dotenv()
app = Flask(__name__)

# Ativa sessões em Flask
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

API_KEY = os.getenv("TOGETHER_API_KEY")
API_URL = "https://api.together.xyz/inference"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

PROMPT_SYSTEM = """
You are a helpful, friendly travel assistant.
Respond in a warm and informative way.
Ask follow-up questions if useful.
"""

def build_prompt(messages):
    system = (
        "You are a helpful, friendly travel assistant that remembers past details.\n"
        "When creating itineraries, format the response with:\n"
        "- Day headers (e.g. '📅 Dia 1 - 31/05')\n"
        "- Bullet points with **bold time**, activity, and place\n"
        "- Use clear line breaks and spacing for readability\n"
        "- Write in European Portuguese\n"
    )
    chat_history = "\n".join([f"{m['role']}: {m['content']}" for m in messages])
    return f"{system}\n{chat_history}\nAssistant:"



@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")

    # Inicializa histórico
    if "chat_history" not in session:
        session["chat_history"] = []

    # Guarda a pergunta do utilizador
    session["chat_history"].append({"role": "User", "content": user_input})

    def get_response(prompt):
        payload = {
            "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",
            "prompt": prompt,
            "max_tokens": 800,
            "temperature": 0.7,
            "top_k": 50,
            "top_p": 0.7,
            "stop": ["User:", "Assistant:"]
        }

        res = requests.post("https://api.together.xyz/v1/completions", headers=HEADERS, json=payload)
        if res.ok:
            result = res.json()
            return result.get("choices", [{}])[0].get("text", "").strip()
        return None

    # Primeira parte
    prompt = build_prompt(session["chat_history"])
    reply_full = get_response(prompt)

    # Tenta continuar até um limite de partes
    for _ in range(2):  # Limita a 2 continuação (podes aumentar)
        if reply_full and not reply_full.strip().endswith((".", "!", "?", "\"")):
            # Pede continuação
            session["chat_history"].append({"role": "Assistant", "content": reply_full})
            session["chat_history"].append({"role": "User", "content": "Continua."})
            prompt = build_prompt(session["chat_history"])
            continuation = get_response(prompt)
            if continuation:
                reply_full += " " + continuation
            else:
                break
        else:
            break

    # Guarda a resposta final
    session["chat_history"].append({"role": "Assistant", "content": reply_full})

    return jsonify({"reply": reply_full})


if __name__ == "__main__":
    app.run(debug=True)
