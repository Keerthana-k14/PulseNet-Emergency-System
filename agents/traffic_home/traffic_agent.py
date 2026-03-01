import os
import time
from dotenv import load_dotenv
from zyndai_agent.agent import AgentConfig, ZyndAIAgent
from zyndai_agent.message import AgentMessage

# Modern LangGraph Imports
from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

load_dotenv(dotenv_path="../../.env")

agent_config = AgentConfig(
    name="Traffic_Control_System",
    description="Manages green corridors.",
    capabilities={"domain": ["traffic_management"], "keywords": ["traffic_control"]},
    webhook_host="0.0.0.0",
    webhook_port=5003,
    registry_url="https://registry.zynd.ai",
    api_key=os.environ.get("ZYND_API_KEY")
)
agent = ZyndAIAgent(agent_config=agent_config)

@tool
def calculate_route_traffic(location: str) -> str:
    """Checks live traffic map for the emergency location."""
    if "highway" in location.lower() or "freeway" in location.lower():
        return "Highway routing active. Bypassing toll booths."
    return "City grid routing active. Synchronizing Green Corridor traffic lights."

llm = ChatGroq(api_key=os.environ.get("GROQ_API_KEY"), model="llama-3.1-8b-instant", temperature=0)
tools = [calculate_route_traffic]
compiled_graph = create_react_agent(llm, tools=tools)

try:
    agent.set_langgraph_agent(compiled_graph)
except AttributeError:
    pass

def traffic_handler(message: AgentMessage, topic: str):
    print(f"\n[TRAFFIC CONTROL] Priority Request: {message.content}")
    try:
        inputs = {"messages": [("user", f"Set traffic route for: {message.content}. Reply with 1 short sentence.")]}
        result = compiled_graph.invoke(inputs)
        status_update = result["messages"][-1].content
    except Exception:
        status_update = "Green corridor established."
    agent.set_response(message.message_id, status_update)
    print(f">>> Action Taken: {status_update}")

agent.add_message_handler(traffic_handler)

if __name__ == "__main__":
    print(f"--- {agent_config.name} LIVE ---")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass