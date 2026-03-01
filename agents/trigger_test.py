import os
import sys
import time
from dotenv import load_dotenv
from zyndai_agent.agent import AgentConfig, ZyndAIAgent

load_dotenv(dotenv_path="../.env")

trigger_config = AgentConfig(
    name="Emergency_Caller",
    description="Trigger script to simulate a 911 emergency app.",
    capabilities={"keywords": ["trigger_script"]},
    webhook_host="0.0.0.0",
    webhook_port=5006,
    registry_url="https://registry.zynd.ai",
    api_key=os.environ.get("ZYND_API_KEY")
)

caller_agent = ZyndAIAgent(agent_config=trigger_config)

results = caller_agent.search_agents_by_keyword("emergency_intake", limit=1)

if results:
    coordinator_target = results[0]
    emergency_details = sys.argv[1] if len(sys.argv) > 1 else "Major traffic collision at Main St."
    
    caller_agent.connect_agent(coordinator_target)
    caller_agent.send_message(emergency_details)
else:
    print("CRITICAL: Could not find the Coordinator Agent.")

time.sleep(3)