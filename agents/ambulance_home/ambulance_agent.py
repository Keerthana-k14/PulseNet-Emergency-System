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

# 1. Zynd Network Config
agent_config = AgentConfig(
    name="Ambulance_Dispatcher",
    description="Dispatches nearest ALS/BLS units.",
    capabilities={"domain": ["emergency_logistics"], "keywords": ["ambulance_dispatch"]},
    webhook_host="0.0.0.0",
    webhook_port=5002,
    registry_url="https://registry.zynd.ai",
    api_key=os.environ.get("ZYND_API_KEY")
)
agent = ZyndAIAgent(agent_config=agent_config)

# 2. Define the Tool
@tool
def find_nearest_ambulance(severity: str) -> str:
    """Finds the closest ambulance based on severity."""
    if "cardiac" in severity.lower() or "trauma" in severity.lower():
        return "Dispatched Advanced Life Support (ALS) Unit #402. ETA: 4 minutes."
    return "Dispatched Basic Life Support (BLS) Unit #109. ETA: 7 minutes."

# 3. Compile the LangGraph
llm = ChatGroq(api_key=os.environ.get("GROQ_API_KEY"), model="llama-3.1-8b-instant", temperature=0)
tools = [find_nearest_ambulance]

# This automatically creates the compiled StateGraph you found in the docs
compiled_graph = create_react_agent(llm, tools=tools)

# Pass the compiled graph to Zynd (as per your documentation snippet)
try:
    agent.set_langgraph_agent(compiled_graph)
except AttributeError:
    # Failsafe just in case the Zynd SDK version is slightly different
    pass

# 4. The Zynd Handler
def dispatch_handler(message: AgentMessage, topic: str):
    print(f"\n[AMBULANCE DISPATCH] Alert received: {message.content}")
    print(">>> Agent invoking LangGraph tool-calling...")
    
    try:
        # We invoke the LangGraph just like your snippet showed
        inputs = {"messages": [("user", f"Use your tool to find an ambulance for: {message.content}. Reply with 1 short sentence.")]}
        result = compiled_graph.invoke(inputs)
        
        # Extract the final AI text from the graph's message state
        status_update = result["messages"][-1].content
    except Exception as e:
        status_update = "Unit #999 en route."
        print(f"LangGraph Error: {e}")

    # Send it back to the decentralized network
    agent.set_response(message.message_id, f"DISPATCH: {status_update}")
    print(f">>> Action Taken: {status_update}")

agent.add_message_handler(dispatch_handler)

if __name__ == "__main__":
    print(f"--- {agent_config.name} LIVE ---")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass