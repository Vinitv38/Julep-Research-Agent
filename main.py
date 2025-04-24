from fastapi import FastAPI, Request
from pydantic import BaseModel
from julep import Julep
import os, yaml, time
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], #for developement, allowing all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = Julep(api_key=os.getenv("JULEP_API_KEY"))

# Creating an agent
agent = client.agents.create(
    name="Research Assistant",
    model="claude-3.5-sonnet",
    about="You are a helpful research assistant. Your goal is to find concise information on topics provided by the user."
)

# Task definition
task_definition = yaml.safe_load("""
name: Research Request
description: Perform research on a given topic and format
main:
- prompt:
  - role: system
    content: >
      You are a research assistant. Return research results strictly and only in one of the selected format the user asks for:
      - summary: 3-4 sentences
      - bullet points: max 5 points
      - short report: max 150 words
  - role: user
    content: "$ f'Please provide a {steps[0].input.output_format} on the topic: {steps[0].input.topic}'"
""")

task = client.tasks.create(agent_id=agent.id, **task_definition)

class ResearchQuery(BaseModel):
    topic: str
    format: str

@app.post("/research")
async def research(query: ResearchQuery):
    print(query.topic, query.format)
    try:
        execution = client.executions.create(
            task_id=task.id,
            input={"topic": query.topic, "output_format": query.format}
        )
        while (result := client.executions.get(execution.id)).status not in ['succeeded', 'failed']:
            time.sleep(1)

        if result.status == 'succeeded':
            output_text = result.output["choices"][0]["message"]["content"]
            return {"result": output_text}

        else:
            return {"error": result.error}

    except Exception as e:
        return {"error": str(e)}
    
@app.get("/")
def home():
    return {
        "message": "Welcome to the Julep Research !",
        "usage": "POST /research with {'topic': '...', 'format': 'summary|bullet points|short report'}",
        "docs": "/docs for Swagger UI"
    }

