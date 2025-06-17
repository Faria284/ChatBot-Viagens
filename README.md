# 🌍 VoyageBot – Assistente de Viagens com LLM

Este projeto foi desenvolvido no âmbito da Unidade Curricular de **Aprendizagem Organizacional - Opção II** (3º ano – Licenciatura em Engenharia Informática, ESTG | IPVC). O **VoyageBot** é um chatbot inteligente capaz de responder a perguntas sobre viagens e gerar roteiros turísticos personalizados com recurso a **LLMs (Large Language Models)**.

## Demonstração Online
A aplicação está disponível online em:  
[https://voyagebot.onrender.com](https://voyagebot.onrender.com)

---

## Como configurar o projeto localmente

Siga os passos abaixo para correr o **VoyageBot** no seu ambiente local:

### 1. Pré-requisitos

Certifique-se de que tem instalado:

- Python 3.8 ou superior
- `pip` (gerenciador de pacotes Python)
- Git

### 2. Clonar o repositório

```bash
git clone https://github.com/Faria284/ChatBot-Viagens.git
cd ChatBot-Viagens
```

### 3. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 4. Configurar as variáveis de ambiente (API Keys)

Crie um ficheiro .env na raíz do projeto com as suas chaves:

**TOGETHER_API_KEY**=YOUR_TOGETHER_API_KEY
**SERPAPI_KEY**=YOUR_SERPAPI_KEY

### 5. Executar a aplicação

```bash
python app.py
```

---

## Objetivos

### Objetivo Geral
Desenvolver um assistente de viagens inteligente baseado em LLM, com as seguintes capacidades:
- Responder a perguntas relacionadas com viagens.
- Gerar roteiros turísticos personalizados.

### Objetivos Específicos
- Explorar o uso de LLMs para interpretar e responder a linguagem natural.
- Integrar fontes externas como:
  - **Together.ai API** (aceder ao modelo Mixtral 8x7B Instruct e gerar respostas coerentes e personalizadas com base no prompt).
  - **Wikipedia API** (resumos sobre destinos).
  - **SerpAPI** (sugestão de restaurantes reais).
- Detetar automaticamente a intenção da pergunta (roteiro ou informação geral).
- Criar uma interface web responsiva e intuitiva com Flask e Tailwind CSS.

---

## Funcionalidades

- **Compreensão de Linguagem Natural** com LLM (Mixtral 8x7B – Together.ai)
- **Geração Automática de Roteiros Turísticos** com base no destino e número de dias
- **Sugestão de Restaurantes Reais** via SerpAPI
- ℹ**Respostas Informativas** para perguntas como:
  - “Que documentos são necessários para visitar o Canadá?”
  - “Como encontrar voos baratos?”
- **Deteção Automática de Intenção** (roteiro vs. pergunta geral)
- **Interface Web Intuitiva** com histórico de conversas, responsiva e visualmente apelativa

---

## Tecnologias Utilizadas

### Componentes Externos
- **[Together.ai](https://www.together.ai/)** – Acesso ao modelo Mixtral-8x7B-Instruct
- **[Wikipedia API](https://pypi.org/project/wikipedia/)** – Resumos de destinos
- **[SerpAPI](https://serpapi.com/)** – Restaurantes reais com base na localização

### Outros Pacotes
- **Flask** – Web framework leve
- **Flask-Session** – Gestão de sessões
- **Requests** – Comunicação com APIs externas
- **Tailwind CSS** – Estilização da interface web

---

## Exemplos de Perguntas
- `3 dias em Madrid`
- `Quais os documentos para visitar o Brasil?`
- `Como encontrar voos baratos para a cidade **Destino**?`

---

## Dificuldades e Possíveis Melhorias
- Ocorreram respostas fora do contexto em algumas interações (ex: respostas em italiano).
- Melhorias futuras:
  - Suporte a múltiplos idiomas.
  - Validação de datas e voos em tempo real.
  - Integração com mapas e APIs de transporte.

---

## Referências

- [Together.ai](https://www.together.ai/)
- [SerpAPI](https://serpapi.com/)
- [Wikipedia API](https://pypi.org/project/wikipedia/)
- [Flask](https://flask.palletsprojects.com)
- [Tailwind CSS](https://tailwindcss.com/)
- Imagem de fundo: [Freepik](https://img.freepik.com/fotos-premium/aviao-no-ceu-ao-por-do-sol_670147-10325.jpg)
- [ChatGPT](https://chatgpt.com)

---

## Autor

**Diogo Fernandes Faria Nº29259**  
Licenciatura em Engenharia Informática – IPVC  
Contacto: diogofernandesfaria@ipvc.pt  

---

© 2025 – Projeto realizado no âmbito da unidade curricular **Aprendizagem Organizacional - Opção II**
