# 🧠 AcadAlert: ML Inference Microservice

This repository contains the Python FastAPI inference server for the **AcadAlert** digital twin ecosystem. 

**This is a sub-repository.** For the full system architecture, live demo video, and frontend React Native code, please visit the main repository:
👉 **[INSERT LINK TO YOUR MOBILE REPO HERE]**

### 🏗️ Microservice Responsibilities
* **Risk Assessment Engine:** Ingests live telemetry (attendance velocity, historical backlogs, assignment scores) from the core Node.js backend.
* **Predictive Analytics:** Outputs a calculated dropout risk level (Low, Medium, High) and generates contextual, natural-language insights (e.g., advising condonation requests for failing electives).
* **High-Speed Inference:** Built on FastAPI/Uvicorn to ensure sub-second response times for the mobile dashboards.

### Tech Stack
* Python 3.11, FastAPI, Uvicorn, Pydantic