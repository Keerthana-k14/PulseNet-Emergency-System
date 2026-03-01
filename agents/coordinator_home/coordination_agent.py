import os
import time
from dotenv import load_dotenv
from zyndai_agent.agent import AgentConfig, ZyndAIAgent
from zyndai_agent.message import AgentMessage

load_dotenv(dotenv_path="../../.env")

agent_config = AgentConfig(
    name="Coordinator_Agent",
    description="Emergency Master Controller - Primary Entry Point.",
    capabilities={"domain": ["emergency_response"], "role": ["coordinator"], "keywords": ["emergency_intake"]},
    webhook_host="0.0.0.0",
    webhook_port=5000,
    registry_url="https://registry.zynd.ai",
    api_key=os.environ.get("ZYND_API_KEY")
)
agent = ZyndAIAgent(agent_config=agent_config)

def emergency_handler(message: AgentMessage, topic: str):
    print(f"\n[MASTER INTAKE] New Emergency Received: {message.content}")
    results = agent.search_agents_by_keyword("medical_help", limit=1)
    
    if results:
        target = results[0]
        print(f"FOUND: {target.get('name')}. Handing off triage...")
        agent.connect_agent(target)
        agent.send_message(message.content)
        agent.set_response(message.message_id, "Emergency received. Triage activated.")

agent.add_message_handler(emergency_handler)

if __name__ == "__main__":
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass