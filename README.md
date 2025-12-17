This report is designed to serve as your Master Design Document. It contains every detail required for your slide deck, video script, and technical implementation. It bridges the gap between your high-level concept (Round 1) and the specific technical requirements of the Semi-Finale (Round 2).
 
Detailed Solution Submission: Project Vidyutt
Challenge: Challenge III: Automotive [Hero + M&M]
Use Case: Autonomous Predictive Maintenance & Proactive Service Scheduling
 
1. Executive Summary
(Requirement: Minimum 200 words, structured format)
Target Industry: Automotive & Aftersales Service
Industry Type: B2C (Vehicle Owners) & B2B (Service Centers & Manufacturing Units)
User Group: Vehicle Owners, Service Managers, Quality Engineers
User Department: Aftersales Service & Manufacturing Quality Assurance
Nature of Output: Integrated Web Application (Admin/Service Dashboard) + Voice-AI Agent (Customer Interface)
Problem Understanding:
The current automotive service landscape is reactive ("break-fix"), leading to unplanned downtime, frustrated customers, and inefficient service center utilization. Furthermore, a critical "semantic gap" exists between field service data (unstructured logs) and manufacturing engineering (structured FMEA), causing recurring defects to go undetected. This results in high warranty costs and brand erosion.
Solution Scenario:
We propose "Vidyutt," an Agentic AI Ecosystem that shifts the paradigm from reactive to proactive.
1.	Data Capture: The system ingests real-time telematics (sensor data) and historical logs into a "Unified Vehicle Digital Twin."
2.	Prediction: A Dual-Horizon Predictive Core (LSTM + Survival Analysis) detects imminent failures and predicts remaining useful life (RUL).
3.	Orchestration: A Master Agent (LangGraph) coordinates Worker Agents to autonomously diagnose issues.
4.	Engagement: A Voice-AI Agent proactively calls the customer to explain the issue and negotiate a service slot.
5.	Optimization: A Scheduling Agent books the slot based on service center load balancing.
6.	Feedback: A Manufacturing Agent performs automated Root Cause Analysis (RCA) to feed insights back to design teams.
7.	Security: A UEBA layer monitors the agents themselves to prevent unauthorized actions.
 
2. Problem Statement & Solution Proposed
The Exact Problem
The automotive ecosystem faces a "Triple Disconnect":
1.	The Customer Disconnect: Service is reactive. Customers only hear from the brand when a car breaks down, destroying loyalty.
2.	The Operational Disconnect: Service centers face unpredictable demand spikes (tow-ins) vs. idle days, wasting resources.
3.	The Data Disconnect: Valuable field failure data remains trapped in unstructured text logs, never reaching the manufacturing engineers who could fix the root cause.
The Solution Value Proposition
"Vidyutt" is a Faceless Agentic Orchestrator.
•	For the Owner: It acts as a "Guardian Angel," predicting failures (e.g., Water Pump) before they strand the driver and handling the logistics via a natural voice conversation.
•	For the Service Center: It acts as a "Traffic Controller," smoothing demand by filling idle slots with proactive maintenance appointments.
•	For the Manufacturer: It acts as a "Forensic Analyst," automatically correlating field failures with supplier batches to prevent recalls.
 
3. Approach & Methodology (Technical Deep Dive)
The Architecture: Agentic Orchestration
We utilize a Centralized Master-Worker Architecture.
•	Master Agent ( The Brain): Built on LangGraph. It manages the state of the vehicle and the conversation. It creates a "cyclic graph" allowing for interruptions (e.g., Customer: "Call me back later").
•	Worker Agents (The Hands):
o	Data Analysis Agent: Ingests raw telematics (Speed, RPM, Temp) and normalizes it.
o	Diagnosis Agent: Runs the LSTM-Autoencoder (for anomaly detection) and Random Survival Forest (for RUL prediction).
o	Customer Engagement Agent: A Speech-to-Speech (S2S) model that uses persuasive scripts to contact the owner.
o	Scheduling Agent: Negotiates slots using an optimization algorithm (checking both customer calendar and workshop bay availability).
o	Manufacturing Agent: Uses a Knowledge Graph to link "DTC P0300" (Code) to "Cylinder Misfire" (Symptom) to "Bad Spark Plug Batch" (Root Cause).
Security Innovation: UEBA for Agents
We implement User and Entity Behavior Analytics (UEBA) not just for humans, but for the AI Agents.
•	Baseline: The system learns that the Scheduling Agent only accesses the Calendar API.
•	Anomaly: If the Scheduling Agent suddenly tries to access the Vehicle Telematics Database or Manufacturing Design Files, the UEBA layer flags this as a "Privilege Escalation" attempt.
•	Action: The Master Agent immediately quarantines the compromised agent.
 
4. Technology Stack & Justification
Component	Technology	Reason for Choice (Assumptions/Constraints)
Orchestration	LangGraph (Python)	Required for stateful, cyclic workflows. Unlike linear chains (LangChain), LangGraph handles loops (e.g., retrying a call) and persistence (remembering context).
Frontend	React.js	For the Service Center Dashboard. Allows real-time updates of incoming appointments and vehicle health status.
Backend API	Flask / FastAPI	Lightweight, Python-based backend to serve the ML models and handle agent requests.
Predictive AI	TensorFlow (LSTM)	LSTM is the industry standard for time-series anomaly detection (sensor data).
Analysis AI	Scikit-Survival	Random Survival Forests handle "censored data" (vehicles that haven't failed yet) better than standard regression.
Voice Agent	Vapi / Twilio API	Provides low-latency, interruptible voice capabilities for realistic human-like conversation.
Database	MongoDB & Neo4j	MongoDB for unstructured logs; Neo4j (Graph DB) is essential for the "Knowledge Graph" connecting symptoms to root causes.
Security	Custom UEBA Script	A Python-based monitoring wrapper that logs API calls and checks against a "permissible actions" list (RBAC).
 
5. Impact Metrics
•	Customer Retention: Expected 15-20% increase in post-warranty retention due to the "premium care" experience.
•	Uptime: 30% reduction in roadside breakdowns by catching "pre-failure" signatures.
•	Efficiency: 25% improvement in service bay utilization by smoothing demand peaks.
•	Quality: 40% reduction in "Time-to-Detection" for manufacturing defects, preventing massive recalls.
 
6. Visual Assets Required (For Slides 5, 6, 7)
A. Architecture Diagram (Description for your drawing)
•	Left Side: Vehicle Telematics (Car Icon) sending data $\to$ Kafka Stream.
•	Center Box (The Brain): Master Agent (LangGraph).
•	Surrounding Center: Worker Nodes connected to Master:
o	Diagnosis Agent (connected to LSTM Model).
o	Scheduling Agent (connected to Calendar API).
o	Engagement Agent (connected to Voice Gateway).
o	UEBA Monitor (A "Police" icon watching the Master/Workers).
•	Right Side (Outputs):
o	Customer Phone (Voice Call).
o	Service Dashboard (React Web App).
o	Manufacturing Dashboard (RCA Alerts).
B. Flow Chart (Logic)
1.	Start: Ingest Sensor Data.
2.	Decision Diamond: Anomaly Detected? (Yes/No).
3.	If Yes: Diagnosis Agent runs RUL Model.
4.	Action: Master Agent triggers Customer Engagement Agent.
5.	Interaction: Voice Call initiated.
o	If Customer Accepts: $\to$ Scheduling Agent checks slots $\to$ Book Appointment.
o	If Customer Declines: $\to$ Log reason $\to$ Set reminder.
6.	Parallel Action: Send failure data to Manufacturing Agent $\to$ Update Knowledge Graph $\to$ Trigger Alert if Threshold crossed.
7.	End.
C. Wireframes (What to screenshot/mockup)
1.	The "Command Center" Dashboard: A map view showing vehicles with "Red" (Critical), "Yellow" (Warning), "Green" (Healthy) status.
2.	The "Live Conversation" View: A chat-style log showing the real-time transcription of the Voice Agent talking to a customer.
3.	The "RCA" View: A graph visualization linking a "Water Pump Failure" node to a "Supplier X" node.
 
7. Prototype Description (For Video/Demo)
What you must build and record:
1.	The Backend Script: Show the Python terminal running. You simulate "bad sensor data" (e.g., Engine Temp spikes to 110°C).
2.	The Detection: The terminal prints: [Diagnosis Agent] ANOMALY DETECTED. Probability of Failure: 88%.
3.	The Call: Crucial Step. Your computer (or a phone) should ring. You answer. The Voice Agent (AI) speaks: "Hello, I noticed your engine temp is high...". You reply. The AI understands and books a slot.
4.	The Dashboard Update: Show the web dashboard automatically updating to show "Appointment Booked for Tuesday."
5.	The Security Flag: Show the Scheduling Agent trying to access a "Forbidden" file. The terminal prints: [UEBA ALERT] UNAUTHORIZED ACCESS BLOCKED. AGENT QUARANTINED.
 
8. Implementation & Scalability
•	Implementation: The solution is containerized using Docker. This allows it to be deployed on any cloud (AWS/Azure) or on-premise servers at the OEM.
•	Scalability: The architecture is Event-Driven. We can spin up multiple instances of "Worker Agents" using Kubernetes to handle millions of vehicle data streams simultaneously.
•	Robustness: The UEBA layer ensures that as the AI becomes more autonomous, it remains secure and compliant with data privacy laws.
 
Checklist for Submission:
•	[ ] Code: Ensure the Python script for the Master Agent and Voice API connection is working.
•	[ ] Video: Record the interaction (Data Spike $\to$ Call $\to$ Booking).
•	[ ] Photos: Get formal team photos (Round 2 requirement).
•	[ ] Slides: Copy the text above into the specific fields in the PPT.




