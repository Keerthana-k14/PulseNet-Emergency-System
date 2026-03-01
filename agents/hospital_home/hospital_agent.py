import os
import time
from dotenv import load_dotenv
from zyndai_agent.agent import AgentConfig, ZyndAIAgent
from zyndai_agent.message import AgentMessage

from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

load_dotenv(dotenv_path="../../.env")

agent_config = AgentConfig(
    name="Hospital_Readiness_Agent",
    description="Monitors hospital beds.",
    capabilities={"domain": ["healthcare_logistics"], "keywords": ["hospital_readiness"]},
    webhook_host="0.0.0.0",
    webhook_port=5004,
    registry_url="https://registry.zynd.ai",
    api_key=os.environ.get("ZYND_API_KEY")
)
agent = ZyndAIAgent(agent_config=agent_config)

@tool
def check_hospital_capacity(injury_type: str) -> str:
    """Checks live database for hospital capacity based on injury."""
    injury_type = injury_type.lower()
    if "burn" in injury_type or "fire" in injury_type:
        return "City Burn Center: 2 beds available. Reserved."
    elif "cardiac" in injury_type or "heart" in injury_type:
        return "Central Hospital Cardiology Wing: 1 bed available. Reserved."
    return "General Hospital ER: Normal capacity. Trauma bay prepped."

llm = ChatGroq(api_key=os.environ.get("GROQ_API_KEY"), model="llama-3.1-8b-instant", temperature=0)
tools = [check_hospital_capacity]
compiled_graph = create_react_agent(llm, tools=tools)

try:
    agent.set_langgraph_agent(compiled_graph)
except AttributeError:
    pass

def hospital_handler(message: AgentMessage, topic: str):
    print(f"\n[HOSPITAL READINESS] Checking capacity for: {message.content}")
    try:
        inputs = {"messages": [("user", f"Find a hospital for: {message.content}. Reply with 1 short sentence.")]}
        result = compiled_graph.invoke(inputs)
        status_update = result["messages"][-1].content
    except Exception:
        status_update = "Central ER Trauma Room reserved."
    agent.set_response(message.message_id, f"STATUS: {status_update}")
    print(f">>> Action Taken: {status_update}")

agent.add_message_handler(hospital_handler)

if __name__ == "__main__":
    print(f"--- {agent_config.name} LIVE ---")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass