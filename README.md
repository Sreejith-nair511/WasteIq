# 🧩 WasteIQ Simulated Backend (FastAPI Mock Server)

A complete FastAPI backend simulation for WasteIQ (OpenCity AI Hub) that mimics the real backend's endpoints and complex outputs — but runs locally without any Docker, database, Redis, Celery, or API keys.

This backend is a mocked simulation, intended for UI and frontend testing. It responds instantly with realistic, detailed JSON outputs for all endpoints.

## 🎯 Objective

Create a single Python FastAPI project that:
- Returns mocked but complex JSON data for all major WasteIQ features
- Has no dependencies on external APIs, DBs, or env vars
- Runs instantly with: `uvicorn main:app --reload`
- Uses random or pre-filled data to simulate intelligent responses

## ⚙️ Tech Stack

- Python 3.11+
- FastAPI
- Uvicorn
- Pydantic
- Faker (for mock data)

## 🗂️ Project Structure

```
wasteiq_sim/
 ├── main.py
 ├── requirements.txt
 └── README.md
```

## 🚀 Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the server:
```bash
uvicorn main:app --reload
```

3. Open the API documentation:
[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## 🧩 Endpoints

All endpoints return simulated data without any external dependencies:

### AUTH
- `POST /api/v1/auth/register` - Register a new user
- `POST /api/v1/auth/login` - Login user

### INFERENCE
- `POST /api/v1/inference/image` - Simulate waste image classification
- `POST /api/v1/inference/chat` - Simulate AI chat responses

### CCTV
- `POST /api/v1/cctv/upload` - Upload CCTV video for processing
- `GET /api/v1/cctv/status/{job_id}` - Get processing status

### INDUSTRIAL EXCHANGE
- `POST /api/v1/industrial/listings` - Add industrial waste listing
- `GET /api/v1/industrial/match` - Get matching buyers

### ANALYTICS
- `GET /api/v1/analytics/summary` - Get waste analytics summary
- `POST /api/v1/analytics/forecast` - Get waste tonnage forecast

### ROUTE OPTIMIZATION
- `POST /api/v1/routes/optimize` - Optimize waste collection routes

### LOGS
- `GET /api/v1/logs` - Get system logs

### WASTE COLLECTION MANAGEMENT
- `POST /api/v1/collections` - Create a new waste collection record
- `GET /api/v1/collections` - List waste collection records
- `GET /api/v1/collections/{collection_id}` - Get a specific collection record

### VEHICLE TRACKING
- `GET /api/v1/vehicles` - List all vehicles with their current status
- `GET /api/v1/vehicles/{vehicle_id}` - Get a specific vehicle's status

### USER MANAGEMENT
- `GET /api/v1/users` - List all users in the system

### REPORT GENERATION
- `POST /api/v1/reports/generate` - Generate a report of specified type

### NOTIFICATIONS
- `GET /api/v1/notifications` - List all notifications
- `POST /api/v1/notifications/{notification_id}/read` - Mark a notification as read

### DASHBOARD
- `GET /api/v1/dashboard/metrics` - Get key metrics for the dashboard

## 🧠 Logic Rules

- No .env, Docker, or DB dependencies
- Uses hardcoded or randomly generated JSON objects
- Each route has example JSON response and status code 200
- Includes simulated complexity (nested data, realistic fields)
- Contains docstrings & comments explaining what each route simulates

## ✅ Acceptance Criteria

- Runs locally without setup
- Returns valid JSON for all routes
- Includes OpenAPI docs automatically
- Contains detailed mock outputs for all major features

## 📖 Example Responses

### POST /api/v1/inference/image
```json
{
  "job_id": "job_9123",
  "status": "completed",
  "result": {
    "predicted_label": "plastic",
    "confidence": 0.94,
    "image_url": "https://mockstorage/waste/job_9123.jpg"
  }
}
```

### POST /api/v1/inference/chat
```json
{
  "reply": "[Simulated AI]: Based on your query, please segregate recyclable waste properly.",
  "model_used": "mistral-7b-instruct",
  "tokens_used": 82
}
```

### GET /api/v1/analytics/summary
```json
{
  "ward": "Ward-12",
  "total_collected": 12000,
  "segregation_rate": "88%",
  "overflow_events": 7,
  "top_waste_types": ["organic", "plastic", "metal"]
}
```

### GET /api/v1/dashboard/metrics
```json
{
  "total_waste_collected": 45872.31,
  "recycling_rate": 82.5,
  "co2_saved": 32450.22,
  "active_wards": 15,
  "alerts": 3
}
```

## 🔚 Notes

Everything is lightweight, fully self-contained, and runnable instantly — no secrets, no external dependencies, all simulated.