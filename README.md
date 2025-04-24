# 🧠 Julep AI Research Assistant API

This project is a FastAPI-based web application that exposes a RESTful API endpoint powered by an AI research agent. Built using the Julep platform and optionally enhanced with real-time search tools like DuckDuckGo, the agent performs topic research and presents the findings in structured formats — such as summaries, bullet points, or short reports.

---

## 🚀 Features

- 🔍 Real-time topic research via Julep AI agent
- 📌 Output formats: `summary`, `bullet points`, `short report`
- ⚡ FastAPI backend with async support
- 🌐 Interactive documentation via Swagger UI
- ☁️ Deployed on [vercel.app](https://vercel.app) for public access

---

## 🗂️ Project Structure

```
.
├── main.py             # Main FastAPI app
├── .env                # Environment variables (JULEP_API_KEY, etc.)
├── .gitignore
├── requirements.txt    # Python dependencies
├── vercel.json         # (Optional) Vercel config
└── README.md           # You're reading it!
```

---

## 📥 API Usage

### ▶️ Endpoint

> `POST /research`

### 📦 Request JSON Body

```json
{
  "topic": "Quantum Computing Basics",
  "output_format": "summary"
}
```

### 📟 Accepted Output Formats

| Format        | Description                           |
|---------------|---------------------------------------|
| `summary`     | 3–4 sentence concise explanation       |
| `bullet points` | Up to 5 clear, structured bullet points |
| `short report` | A ~150-word brief report on the topic  |

---

### ✅ Example Response

```json
{
  "result": "Quantum computing leverages quantum bits..."
}
```

---

## 🧪 Try It Live

> **Swagger UI** available at  
> [https://julep-research-agent.vercel.app/docs](https://julep-research-agent.vercel.app/docs)

This lets users test the API directly from the browser with a live UI.

---

## ⚙️ Local Development

### 1. Clone the Repository

```bash
git clone https://github.com/Vinitv38/Julep-Research-Agent.git
cd Julep-Research-Agent
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Add Environment Variables

Create a `.env` file in the root:

```
JULEP_API_KEY=your_julep_api_key
JULEP_ENVIRONMENT=production
```

### 4. Start the Server

```bash
uvicorn main:app --reload
```

> Visit: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 🧠 Technologies Used

- [Julep AI](https://docs.julep.ai) – Agent configuration & orchestration
- [FastAPI](https://fastapi.tiangolo.com/) – Python web framework
- [Uvicorn](https://www.uvicorn.org/) – ASGI server
- `.env` + `python-dotenv` for configuration

---

## 🛠️ Future Enhancements

- [ ] Add DuckDuckGo or Brave search tool
- [ ] Enable streaming responses

---

## 👤 Author

**Vinit Lathiwala**  
[GitHub](https://github.com/vinitlathiwala) | [LinkedIn](https://linkedin.com/in/your-profile)

---

## 📄 License

MIT License — free to use, fork, and adapt.
