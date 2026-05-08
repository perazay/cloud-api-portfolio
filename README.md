# Cloud REST API (Google Cloud Run + Cloud SQL)

I built a backend REST API using Flask, Docker, and Google Cloud Run, connected to a MySQL database (Cloud SQL).  
This project helped me understand how real backend services are deployed, connected to databases, and debugged in the cloud.

---

## Live Demo

https://api-547965439790.us-central1.run.app

---

## What this project does

- Runs a REST API in the cloud using Cloud Run  
- Connects to a MySQL database (Cloud SQL)  
- Supports full CRUD operations  
- Includes endpoints to test system health, failures, and slow responses  

---

## How it works

- I containerized the app using Docker  
- Deployed it using Google Cloud Run  
- Connected it to Cloud SQL using a secure socket  
- Used Gunicorn to run it like a real production service  

## API Endpoints

| Endpoint | Method | What it does |
|--------|--------|------------|
| `/` | GET | Basic “API is running” message |
| `/health` | GET | Checks if API + database are working |
| `/items` | GET | Gets items (with pagination) |
| `/items` | POST | Creates a new item |
| `/items/<id>` | GET | Gets one item |
| `/items/<id>` | PUT | Updates an item |
| `/items/<id>` | DELETE | Deletes an item |
| `/simulate-failure` | GET | Forces an error (used for testing) |
| `/slow` | GET | Delays response (used to test performance) |

---

## What I focused on

Instead of just building an API, I wanted to understand how systems behave in real situations:

- Added a `/health` endpoint to check if everything is working  
- Created a failure endpoint to see how errors behave  
- Added a slow endpoint to simulate latency  
- Used logging to help debug issues  

---

## Database

- Google Cloud SQL (MySQL)  
- Connected using SQLAlchemy  
- Handles full CRUD operations  
- Verified connection using the `/health` endpoint  

---

## 💻 Run it locally

```bash
docker build -t api .
docker run -p 8081:8080 api
```
Open:
```bash
https://localhost:8081
```
---

## Deploy 

```bash
gcloud run deploy api \
  --source . \
  --region us-central1 \
  --allow-unauthenticated
```
---
## Screenshots 

View all screenshots here: [Screenshots](screenshots.md)

---

## What I learned 
- How to deploy a containerized app to the cloud
- How to connect Cloud Run to Cloud SQL
- How to debug cloud deployment and permission issues
- How backend systems handle failures and slow responses
- How to design APIs that are closer to real-world systems 
---

## About Me
Yuritzia Peraza 
Computer Sciece @ Oregon State University