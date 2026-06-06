# 🧠 AcadAlert: ML Inference Microservice

This repository contains the Python FastAPI inference server for the **AcadAlert** digital twin ecosystem. 

**This is a sub-repository.** For the full system architecture, live demo video, and frontend React Native code, please visit the main repository:
👉 **[LINK TO MOBILE REPO HERE](https://github.com/AcadAlert-Team/acadalert-mobile)**

## 🏗️ Microservice Responsibilities

* **Risk Assessment Engine:** Ingests live telemetry (attendance velocity, historical backlogs, assignment scores) from the core Node.js backend.
* **Predictive Analytics:** Outputs a calculated dropout risk level (Low, Medium, High) and generates contextual, natural-language insights.
* **Production API:** Hosted on an **AWS EC2** instance and managed via **PM2** alongside the Node.js core, utilizing FastAPI/Uvicorn to ensure continuous, sub-second response times for the mobile dashboards.

## 🛠️ Tech Stack
Python 3.11, FastAPI, Uvicorn, Pydantic, Scikit-learn, AWS EC2, PM2

