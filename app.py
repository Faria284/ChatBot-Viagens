import os
import re
import requests
import wikipedia
from flask import Flask, render_template, request, jsonify, session
from flask_session import Session
from dotenv import load_dotenv
from langdetect import detect

# Configuração base
wikipedia.set_lang("pt")
load_dotenv()
SERPAPI_KEY = os.getenv("SERPAPI_KEY")
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")

# Flask app
app = Flask(__name__)
app.secret_key = "supersecretkey"
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

MODEL = "mistralai/Mixtral-8x7B-Instruct-v0.1"
HEADERS = {
    "Authorization": f"Bearer {TOGETHER_API_KEY}",
    "Content-Type": "application/json"
}



def detect_language(text):
    try:
        lang = detect(text)
        return lang
    except:
        return "pt"
    


def extract_location(text):
    pattern = r"(?:em|para|visitar|viajar para)\s+([A-ZÀ-Ü][\w\s'\u2019\-]+)"
    matches = re.findall(pattern, text, re.IGNORECASE)
    if matches:
        return matches[-1].strip().title()
    return None



def get_restaurants(city="Lisboa", country="Portugal"):
    SERPAPI_KEY = os.getenv("SERPAPI_KEY")
    if not SERPAPI_KEY:
        return []

    params = {
        "engine": "google",
        "q": f"restaurantes em {city}, {country}",
        "location": f"{city}, {country}",
        "api_key": SERPAPI_KEY,
        "hl": "pt"
    }

    response = requests.get("https://serpapi.com/search", params=params)
    if response.status_code != 200:
        print(f"[ERRO] SerpAPI: {response.text}")
        return []

    results = response.json()
    places = results.get("local_results", {}).get("places", [])
    return [f"{p.get('title')} – {p.get('address', '')}" for p in places if p.get("title")]



def detetar_intencao(user_input):
    user_input = user_input.lower()
    if re.search(r"\b(roteiro|plano|itinerário|viajar para|visitar|o que ver em)\b", user_input):
        return "roteiro"
    if re.search(r"\b(voos?|bilhetes|documentos|destinos|dicas|mochila|viajar sozinho|passaporte|vistos?)\b", user_input):
        return "info"
    return "desconhecido"



def build_prompt(user_input):
    idioma = detect_language(user_input)
    is_pt = idioma == "pt"
    location = extract_location(user_input)
    num_dias = 3
    resumo = ""
    restaurantes = []
    lista_restaurantes = ""

    if match := re.search(r"(\d+)\s*dias?", user_input.lower()):
        num_dias = int(match.group(1))

    if location:
        restaurantes = get_restaurants(location)
        lista_restaurantes = "\n".join(f"- {r}" for r in restaurantes[:6]) if restaurantes else ""
        try:
            results = wikipedia.search(location)
            if results:
                resumo = wikipedia.summary(results[0], sentences=2)
        except Exception as e:
            resumo = f"(Não foi possível obter informações da Wikipédia: {e})"

    perguntas_informativas = [
        "documentos", "voos", "bilhetes", "viajar sozinho",
        "destinos", "voo barato", "voos baratos", "preciso para viajar", "é necessário para entrar"
    ]
    if any(p in user_input.lower() for p in perguntas_informativas):
        if is_pt:
            return f"""
És um assistente de viagens inteligente e prestável. Responde **em português de Portugal** à seguinte pergunta:

Pergunta: {user_input}

Responde com:
- Informação clara, atualizada e bem formatada (listas, passos, etc.)
- Tom profissional e amigável
- Evita palavras em espanhol (ex: "salud", "el", "mental", etc.)
- **Não cries roteiros**, apenas responde diretamente à pergunta
""".strip()

    # Prompt para roteiro turístico
    return f"""
Cria um roteiro turístico de {num_dias} dias em {location or 'uma cidade portuguesa'} com base na seguinte descrição:

Resumo da cidade:
{resumo}

Sugestões de restaurantes reais:
{lista_restaurantes}

Gera o plano com este formato:
📅 Dia 1
- **09:00** - Local/Atividade
- **11:00** - Local/Atividade
- **13:00** - Almoço no [nome do restaurante]
- ...
Termina o dia com o jantar.

Mantém o idioma utilizado pelo utilizador.
Evita sair do tema ou adicionar textos irrelevantes.
Escreve com clareza e foco no plano turístico.
""".strip()



def resposta_parecida_com_erro(texto):
    if not texto:
        return True
    if len(texto.split()) < 20:
        return True
    irrelevantes = ["pitagora", "salute mentale", "covid", "pandemia", "teorema"]
    contador = sum(1 for palavra in irrelevantes if palavra in texto.lower())
    return contador >= 2



def send_to_together(prompt):
    tentativas = 3
    for _ in range(tentativas):
        payload = {
            "model": MODEL,
            "prompt": prompt,
            "max_tokens": 1000,
            "temperature": 0.7,
            "top_k": 50,
            "top_p": 0.7,
            "stop": ["User:", "Assistant:"]
        }
        res = requests.post("https://api.together.xyz/v1/completions", headers=HEADERS, json=payload)
        if res.ok:
            texto = res.json()["choices"][0]["text"].strip()
            if resposta_parecida_com_erro(texto):
                print("❗ Conteúdo fora do tema detectado, nova tentativa...")
                continue
            return texto
        else:
            print("[ERRO] Resposta da API Together:", res.text)
    return "Ocorreu um erro ao gerar a resposta. Tenta novamente."



@app.route("/")
def index():
    return render_template("index.html")



@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")
    prompt = build_prompt(user_input)
    reply = send_to_together(prompt)

    if "chat_history" not in session:
        session["chat_history"] = []
    session["chat_history"].append({"user": user_input, "bot": reply})
    session["chat_history"] = session["chat_history"][-6:]
    session.modified = True

    return jsonify({"reply": reply, "history": session["chat_history"]})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

