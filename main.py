from fastapi import FastAPI, Request
from pydantic import BaseModel
from julep import Julep
import os, yaml, time
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

client = Julep(api_key=os.getenv("JULEP_API_KEY"))

# Creating an agent
agent = client.agents.create(
    name="Research Assistant",
    model="claude-3.5-sonnet",
    about="You are a helpful research assistant. ..."
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
    output_format: str

@app.post("/research")
async def research(query: ResearchQuery):
    print(query.topic, query.output_format)
    try:
        execution = client.executions.create(
            task_id=task.id,
            input={"topic": query.topic, "output_format": query.output_format}
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
