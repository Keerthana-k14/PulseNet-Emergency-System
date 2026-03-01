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
    name="Doctor_Availability_Agent",
    description="Matches injuries to on-call doctors.",
    capabilities={"domain": ["medical_staffing"], "keywords": ["doctor_availability"]},
    webhook_host="0.0.0.0",
    webhook_port=5005,
    registry_url="https://registry.zynd.ai",
    api_key=os.environ.get("ZYND_API_KEY")
)
agent = ZyndAIAgent(agent_config=agent_config)

@tool
def check_doctor_availability(specialty: str) -> str:
    """Checks the staff roster for on-call specialists."""
    if "burn" in specialty.lower():
        return "Dr. Silva (Burn Specialist) paged to ER."
    elif "cardiac" in specialty.lower():
        return "Dr. Chen (Cardiologist) paged to ER."
    return "Dr. Aris (Trauma Surgeon) paged to ER."

llm = ChatGroq(api_key=os.environ.get("GROQ_API_KEY"), model="llama-3.1-8b-instant", temperature=0)
tools = [check_doctor_availability]
compiled_graph = create_react_agent(llm, tools=tools)

try:
    agent.set_langgraph_agent(compiled_graph)
except AttributeError:
    pass

def doctor_handler(message: AgentMessage, topic: str):
    print(f"\n[DOCTOR AVAILABILITY] Paging staff for: {message.content}")
    try:
        inputs = {"messages": [("user", f"Find a doctor for: {message.content}. Reply with 1 short sentence.")]}
        result = compiled_graph.invoke(inputs)
        status_update = result["messages"][-1].content
    except Exception:
        status_update = "On-call trauma team activated."
    agent.set_response(message.message_id, status_update)
    print(f">>> Action Taken: {status_update}")

agent.add_message_handler(doctor_handler)

if __name__ == "__main__":
    print(f"--- {agent_config.name} LIVE ---")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass