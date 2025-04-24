from fastapi import FastAPI, Request
from pydantic import BaseModel
from julep import Julep
import os, yaml, time
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

client = Julep(api_key=os.getenv("JULEP_API_KEY"))

# Create or fetch your agent here
agent = client.agents.create(
    name="Research Assistant",
    model="claude-3.5-sonnet",
    about="You are a helpful research assistant. ..."
)

task_definition = yaml.safe_load("""
name: Research Request
description: Perform research on a given topic and format
main:
- prompt:
  - role: user
    content: $ f"Topic: {steps[0].input.topic}\\nFormat: {steps[0].input.format}"
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
            input={"topic": query.topic, "format": query.format}
        )
        while (result := client.executions.get(execution.id)).status not in ['succeeded', 'failed']:
            time.sleep(1)

        if result.status == 'succeeded':
            return {"result": result.output}
        else:
            return {"error": result.error}

    except Exception as e:
        return {"error": str(e)}
    
@app.post("/")
def home():
    return {"message": "Welcome to the Julep Research Assistant!"}
