# 🧠 AcadAlert: Data Engineering Platform & ML Engine

This repository contains the Python ETL pipelines and FastAPI inference server for the **AcadAlert** ecosystem, originally a full-stack app now upgraded into a robust Data Engineering Platform.

**This is a sub-repository.** For the full system architecture, live demo video, and frontend React Native code, please visit the main repository:
👉 **[INSERT LINK TO YOUR MOBILE REPO HERE]**

### 🏗️ Data Engineering & Pipeline Features
* **Automated Batch ETL Pipelines:** Utilizes Python and Pandas to extract raw transactional data, transform it (cleansing, feature engineering), and load it into analytics staging schemas.
* **Idempotent Ingestion:** Employs UPSERT (Insert on Conflict DO UPDATE) logic to guarantee pipeline idempotency and prevent data duplication during retries.
* **Fault-Tolerant Architecture:** Integrates with Dead Letter Queues (DLQ) in the core system to capture and retry failed events.
* **Optimized Storage:** Interacts with a strictly normalized (3NF) PostgreSQL database utilizing B-Tree composite and partial indexes for high-speed queries.

### 🧠 Machine Learning Microservice Responsibilities
* **Risk Assessment Engine:** Ingests live telemetry (attendance velocity, historical backlogs, assignment scores) from the core backend.
* **Predictive Analytics:** Outputs a calculated dropout risk level (Low, Medium, High) and generates contextual, natural-language insights (e.g., advising condonation requests for failing electives).
* **High-Speed Inference:** Built on FastAPI/Uvicorn to ensure sub-second response times for the mobile dashboards.

### Tech Stack
* Python 3.11, Pandas, FastAPI, Uvicorn, Pydantic, Supabase (PostgreSQL)