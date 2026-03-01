# 🚨 PulseNet: AI-Powered Emergency Coordination Swarm

PulseNet is a dual-intake AI Emergency Copilot powered by a LangGraph multi-agent swarm and Groq. It automates emergency call dispatch by processing live audio and citizen SOS inputs, instantly delivering life-saving first-aid while coordinating ambulances, traffic routing, and hospital beds in parallel to drastically reduce response times.

## ⚠️ The Problem
Traditional emergency control centers (ECCs) are bottlenecked by linear, manual processes. Human dispatchers must sequentially transcribe the situation, verbally triage the patient, look up hospital bed availability, and contact ambulance routing. In critical incidents, these manual handoffs cost life-saving minutes.

## 💡 Our Solution
PulseNet solves this latency crisis by replacing the linear dispatcher workflow with a parallel AI swarm. By automating data extraction and logistical coordination simultaneously, we eliminate manual data-entry delays. 

It serves two distinct fronts:
1. **Citizen SOS App (User Mode):** Bypasses the standard call queue by allowing users to submit structured data and instantly receive dynamic, LLM-generated first-aid instructions while the physical response is routed in the background.
2. **ECC Copilot (Operator Mode):** Listens to live emergency call audio transcripts, extracts critical data, and prepares a full dispatch plan. The human operator is freed from typing and acts as the final **Verification Gateway** to approve the AI's dispatch plan.

## 🧠 Multi-Agent Architecture



PulseNet utilizes 6 specialized autonomous agents built on the Zynd SDK and LangGraph:
* **Coordinator Agent (Port 5000):** The master intake node that receives the emergency payload and routes it to triage.
* **Medical Agent (Port 5001):** Powered by Groq (`llama-3.1-8b-instant`), it analyzes the emergency, generates immediate first-aid directives, and broadcasts the priority level to the logistics swarm.
* **Ambulance Agent (Port 5002):** Executes tool-calls to dispatch nearest ALS/BLS units.
* **Traffic Agent (Port 5003):** Establishes green corridors and bypasses toll booths.
* **Hospital Agent (Port 5004):** Checks live databases to reserve trauma/burn beds.
* **Doctor Agent (Port 5005):** Pages the correct on-call specialists (e.g., Cardiologist vs. Trauma Surgeon).

## 🛠️ Technology Stack
* **Agent Framework:** Zynd AI Agent SDK (Blockchain DID identity registration)
* **AI Orchestration:** LangGraph (Tool-calling and React agent logic)
* **LLM Inference:** Groq LPU (`llama-3.1-8b-instant` for ultra-low latency generation)
* **Frontend:** Streamlit (Custom enterprise-grade dispatch dashboard)
* **Backend:** Python, Flask, Synchronous Webhooks
* **Target Hardware:** Optimized for **AMD Instinct™ MI300X Accelerators** for secure, on-premise deployment.

## 🚀 Running the Prototype Locally

### Prerequisites
* Python 3.10+
* Groq API Key
* Zynd AI SDK API Key

### Installation & Setup
1. Clone the repository:
   ```bash
   git clone [https://github.com/YourUsername/PulseNet-Emergency-System.git](https://github.com/YourUsername/PulseNet-Emergency-System.git)
   cd PulseNet-Emergency-System
2. Install dependencies:
```bash
pip install -r requirements.txt
````

3. Create a `.env` file in the root directory:

```env
GROQ_API_KEY=your_groq_key_here
ZYND_API_KEY=your_zynd_key_here
```

---

## Execution

Open two terminal windows.

Terminal 1: Start the agent swarm

```bash
python start_all.py
```

Terminal 2: Start the dashboard

```bash
streamlit run agents/dashboard.py
```
