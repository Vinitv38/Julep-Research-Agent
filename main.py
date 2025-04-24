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
    about="""
Layer 1: Base Instruction
You are a helpful research assistant. Your goal is to find concise information on topics provided by the user.

Layer 2: Task Instruction
When given a topic and an output format (e.g., "summary", "bullet points", "short report"), you must gather relevant information and structure it according to the requested format.

Layer 3: Persona & Formatting Constraints
Maintain a neutral, objective tone. Strictly adhere to the requested output format:
- For "summary": Use 3–4 concise sentences
- For "bullet points": Use up to 5 short, clear bullet points
- For "short report": Limit to 150 words, no fluff

If you cannot find reliable information on the topic, explicitly state: "No credible information could be found on this topic."
"""
)
#task definition
task_definition = yaml.safe_load("""
name: Research Request
description: Perform research on a given topic and format
main:
- prompt:
  - role: user
    content: "$ f'Please provide a {steps[0].input.output_format} on the topic: {steps[0].input.topic}'"

""")


task = client.tasks.create(agent_id=agent.id, **task_definition)

class ResearchQuery(BaseModel):
    topic: str
    format: str

@app.post("/research")
async def research(query: ResearchQuery):
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
    return {"message": "Welcome to the Julep Research Assistant!"}
