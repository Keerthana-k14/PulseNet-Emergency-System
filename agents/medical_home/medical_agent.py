import os
import time
from dotenv import load_dotenv
from zyndai_agent.agent import AgentConfig, ZyndAIAgent
from zyndai_agent.message import AgentMessage
from groq import Groq

load_dotenv(dotenv_path="../../.env")

agent_config = AgentConfig(
    name="Medical_Command_Center",
    description="Incident Commander: Provides first-aid and orchestrates response.",
    capabilities={"domain": ["medical_triage"], "keywords": ["medical_help"]},
    webhook_host="0.0.0.0",
    webhook_port=5001,
    registry_url="https://registry.zynd.ai",
    api_key=os.environ.get("ZYND_API_KEY")
)
agent = ZyndAIAgent(agent_config=agent_config)
groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def medical_handler(message: AgentMessage, topic: str):
    print(f"\n[TRIAGE COMMAND] Intake Received: {message.content}")
    print(">>> Analyzing emergency via Groq LLM...")
    
    try:
        completion = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are an AI triage commander. Provide a maximum of 2 sentences of immediate, actionable first-aid advice for the reported emergency. Be direct and calm."},
                {"role": "user", "content": f"Emergency report: {message.content}"}
            ],
            temperature=0.2,
            max_tokens=100
        )
        advice = completion.choices[0].message.content
    except Exception as e:
        advice = "ERROR: LLM unreachable. Keep patient calm and wait for EMS."

    agent.set_response(message.message_id, f"FIRST AID PROTOCOL: {advice}")
    print(f">>> Sent dynamic advice: {advice}")

    support_team = ["ambulance_dispatch", "traffic_control", "hospital_readiness", "doctor_availability"]
    for service in support_team:
        results = agent.search_agents_by_keyword(service, limit=1)
        if results:
            target = results[0]
            agent.connect_agent(target)
            agent.send_message(f"URGENT PRIORITY: {message.content}")

agent.add_message_handler(medical_handler)

if __name__ == "__main__":
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass