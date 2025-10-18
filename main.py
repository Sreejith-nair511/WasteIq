import os
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any, Union
import uuid
import random
from datetime import datetime, timedelta
from faker import Faker
import json

app = FastAPI(title="WasteIQ Simulated Backend", 
              description="Simulated backend for WasteIQ — returns mock responses, ideal for frontend testing.",
              version="1.0.0")

# Add CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

fake = Faker()

# Pydantic models for request/response bodies
class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str
    role: str

class RegisterResponse(BaseModel):
    id: str
    name: str
    email: str
    role: str
    token: str

class LoginRequest(BaseModel):
    email: str
    password: str

class LoginResponse(BaseModel):
    token: str
    user: Dict[str, Any]

class ChatRequest(BaseModel):
    model: str
    messages: List[Dict[str, str]]
    user_id: str

class ChatResponse(BaseModel):
    reply: str
    model_used: str
    tokens_used: int

class CCTVStatusResponse(BaseModel):
    events: List[Dict[str, str]]

class IndustrialListingRequest(BaseModel):
    company: str
    material_type: str
    quantity: float
    location: str

class IndustrialMatchResponse(BaseModel):
    buyer_id: int
    company: str
    similarity: float

class AnalyticsSummaryResponse(BaseModel):
    ward: str
    total_collected: int
    segregation_rate: str
    overflow_events: int
    top_waste_types: List[str]

class ForecastRequest(BaseModel):
    days: int = 7

class ForecastResponse(BaseModel):
    dates: List[str]
    predicted_tonnage: List[float]
    confidence_intervals: List[Dict[str, float]]

class RouteOptimizeRequest(BaseModel):
    locations: List[str]
    vehicle_capacity: int

class RouteOptimizeResponse(BaseModel):
    route_order: List[str]
    total_distance: float
    estimated_time: str
    optimizer_score: float

class LogEntry(BaseModel):
    timestamp: str
    level: str
    message: str
    module: str

# New models for expanded functionality
class WasteCollectionRequest(BaseModel):
    ward: str
    date: str
    vehicle_id: str

class WasteCollectionResponse(BaseModel):
    collection_id: str
    ward: str
    date: str
    total_weight: float
    waste_breakdown: Dict[str, float]
    collector: str
    status: str

class VehicleTrackingResponse(BaseModel):
    vehicle_id: str
    location: Dict[str, float]
    status: str
    last_updated: str
    route_progress: float

class UserManagementResponse(BaseModel):
    users: List[Dict[str, Any]]
    total_count: int
    active_count: int

class ReportGenerationRequest(BaseModel):
    report_type: str
    start_date: str
    end_date: str

class ReportGenerationResponse(BaseModel):
    report_id: str
    report_type: str
    generated_at: str
    data: Dict[str, Any]

class NotificationResponse(BaseModel):
    id: str
    title: str
    message: str
    timestamp: str
    read: bool
    type: str

class DashboardMetricsResponse(BaseModel):
    total_waste_collected: float
    recycling_rate: float
    co2_saved: float
    active_wards: int
    alerts: int

# Helper functions for generating mock data
def generate_mock_token():
    return f"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.{fake.sha256()[:20]}.{fake.sha256()[:20]}"

def generate_user_id():
    return f"user_{fake.uuid4()[:8]}"

def generate_job_id():
    return f"job_{fake.uuid4()[:8]}"

def get_random_waste_type():
    waste_types = ["organic", "plastic", "metal", "glass", "paper", "electronic", "hazardous"]
    return random.choice(waste_types)

def get_random_confidence():
    return round(random.uniform(0.75, 0.99), 2)

def generate_ward_name():
    return f"Ward-{random.randint(1, 50)}"

def generate_vehicle_id():
    return f"VH-{random.randint(1000, 9999)}"

# In-memory storage for mock data
mock_collections = []
mock_vehicles = []
mock_users = []
mock_reports = []
mock_notifications = []

# Initialize mock data
def initialize_mock_data():
    # Generate mock collections
    for _ in range(50):
        waste_types = ["organic", "plastic", "metal", "glass", "paper"]
        breakdown = {}
        total = 0
        for wt in waste_types:
            amount = round(random.uniform(100, 1000), 2)
            breakdown[wt] = amount
            total += amount
        
        mock_collections.append({
            "collection_id": generate_job_id(),
            "ward": generate_ward_name(),
            "date": (datetime.now() - timedelta(days=random.randint(0, 30))).strftime("%Y-%m-%d"),
            "total_weight": round(total, 2),
            "waste_breakdown": breakdown,
            "collector": fake.name(),
            "status": random.choice(["completed", "in_progress", "scheduled"])
        })
    
    # Generate mock vehicles
    for i in range(20):
        mock_vehicles.append({
            "vehicle_id": generate_vehicle_id(),
            "location": {
                "lat": round(random.uniform(12.9, 13.1), 6),
                "lng": round(random.uniform(77.5, 77.7), 6)
            },
            "status": random.choice(["active", "idle", "maintenance"]),
            "last_updated": (datetime.now() - timedelta(minutes=random.randint(0, 120))).isoformat() + "Z",
            "route_progress": round(random.uniform(0, 100), 2)
        })
    
    # Generate mock users
    roles = ["admin", "operator", "supervisor", "manager", "analyst"]
    for i in range(30):
        mock_users.append({
            "id": generate_user_id(),
            "name": fake.name(),
            "email": fake.email(),
            "role": random.choice(roles),
            "status": random.choice(["active", "inactive"]),
            "last_login": (datetime.now() - timedelta(days=random.randint(0, 30))).isoformat() + "Z"
        })
    
    # Generate mock notifications
    notification_types = ["alert", "info", "warning", "success"]
    for i in range(15):
        mock_notifications.append({
            "id": generate_job_id(),
            "title": fake.sentence(nb_words=4),
            "message": fake.sentence(nb_words=10),
            "timestamp": (datetime.now() - timedelta(hours=random.randint(0, 48))).isoformat() + "Z",
            "read": random.choice([True, False]),
            "type": random.choice(notification_types)
        })

# Initialize mock data on startup
initialize_mock_data()

# AUTH ENDPOINTS
@app.post("/api/v1/auth/register", response_model=RegisterResponse)
async def register_user(request: RegisterRequest):
    """
    Simulate user registration.
    Returns a mock user object with a token.
    """
    user_id = generate_user_id()
    token = generate_mock_token()
    
    return RegisterResponse(
        id=user_id,
        name=request.name,
        email=request.email,
        role=request.role,
        token=token
    )

@app.post("/api/v1/auth/login", response_model=LoginResponse)
async def login_user(request: LoginRequest):
    """
    Simulate user login.
    Returns a mock token and user object.
    """
    user_id = generate_user_id()
    token = generate_mock_token()
    
    return LoginResponse(
        token=token,
        user={
            "id": user_id,
            "name": fake.name(),
            "email": request.email,
            "role": random.choice(["admin", "operator", "supervisor"])
        }
    )

# INFERENCE ENDPOINTS
@app.post("/api/v1/inference/image")
async def classify_waste_image(file: UploadFile = File(...)):
    """
    Simulate image classification for waste.
    Accepts an image file and returns mock classification results.
    """
    job_id = generate_job_id()
    predicted_label = get_random_waste_type()
    confidence = get_random_confidence()
    
    return {
        "job_id": job_id,
        "status": "completed",
        "result": {
            "predicted_label": predicted_label,
            "confidence": confidence,
            "image_url": f"https://mockstorage/waste/{job_id}.jpg"
        }
    }

@app.post("/api/v1/inference/chat", response_model=ChatResponse)
async def chat_with_ai(request: ChatRequest):
    """
    Simulate AI chat responses for waste management queries.
    Returns a mock AI-generated reply.
    """
    ai_responses = [
        "[Simulated AI]: Please segregate organic and plastic waste separately.",
        "[Simulated AI]: For electronic waste, please contact your local e-waste collection center.",
        "[Simulated AI]: Composting organic waste can reduce landfill usage by up to 30%.",
        "[Simulated AI]: Recycling one ton of plastic saves approximately 5,774 kWh of energy.",
        "[Simulated AI]: Metal cans should be cleaned before recycling for optimal processing.",
        "[Simulated AI]: Glass can be recycled indefinitely without loss in quality or purity.",
        "[Simulated AI]: Paper recycling can save up to 60% of energy compared to making paper from virgin materials.",
        "[Simulated AI]: Hazardous waste like batteries should be disposed of at designated collection points."
    ]
    
    return ChatResponse(
        reply=random.choice(ai_responses),
        model_used=request.model,
        tokens_used=random.randint(50, 150)
    )

# CCTV ENDPOINTS
@app.post("/api/v1/cctv/upload")
async def upload_cctv_video(file: UploadFile = File(...)):
    """
    Simulate CCTV video upload for processing.
    Returns a job ID and processing status.
    """
    job_id = generate_job_id()
    
    return {
        "job_id": job_id,
        "status": "processing"
    }

@app.get("/api/v1/cctv/status/{job_id}", response_model=CCTVStatusResponse)
async def get_cctv_status(job_id: str):
    """
    Get the status of a CCTV processing job.
    Returns mock event data.
    """
    # Simulate some events with timestamps
    events = []
    base_time = datetime.utcnow() - timedelta(hours=2)
    
    for i in range(random.randint(1, 5)):
        event_time = base_time + timedelta(minutes=i*15)
        event_types = [
            "Overflow detected",
            "Illegal dumping observed",
            "Bin collection completed",
            "Vehicle entry detected",
            "Maintenance required",
            "Lid open detected",
            "Fire hazard detected",
            "Animal intrusion detected"
        ]
        
        events.append({
            "timestamp": event_time.isoformat() + "Z",
            "event": random.choice(event_types)
        })
    
    return CCTVStatusResponse(events=events)

# INDUSTRIAL EXCHANGE ENDPOINTS
@app.post("/api/v1/industrial/listings")
async def add_industrial_listing(request: IndustrialListingRequest):
    """
    Add a mock industrial waste listing.
    Returns a simulated embedding score.
    """
    listing_id = f"listing_{fake.uuid4()[:8]}"
    
    return {
        "id": listing_id,
        "company": request.company,
        "material_type": request.material_type,
        "quantity": request.quantity,
        "location": request.location,
        "embedding_score": round(random.uniform(0.8, 0.99), 3),
        "created_at": datetime.utcnow().isoformat() + "Z"
    }

@app.get("/api/v1/industrial/match", response_model=List[IndustrialMatchResponse])
async def get_industrial_matches():
    """
    Get simulated matches for industrial waste exchange.
    Returns ranked mock buyers.
    """
    companies = [
        "EcoRecycle Ltd",
        "GreenTech Solutions",
        "WasteToWealth Industries",
        "Circular Economy Corp",
        "Sustainable Materials Inc",
        "BioCycle Systems",
        "Renewable Resources Co",
        "Zero Waste Enterprises"
    ]
    
    matches = []
    for i in range(random.randint(3, 7)):
        matches.append(IndustrialMatchResponse(
            buyer_id=i+1,
            company=random.choice(companies),
            similarity=round(random.uniform(0.75, 0.99), 2)
        ))
    
    # Sort by similarity descending
    matches.sort(key=lambda x: x.similarity, reverse=True)
    return matches

# ANALYTICS ENDPOINTS
@app.get("/api/v1/analytics/summary", response_model=AnalyticsSummaryResponse)
async def get_analytics_summary():
    """
    Get summarized waste analytics.
    Returns aggregate metrics for waste management.
    """
    wards = [f"Ward-{i}" for i in range(1, 21)]
    waste_types = ["organic", "plastic", "metal", "glass", "paper", "electronic"]
    
    return AnalyticsSummaryResponse(
        ward=random.choice(wards),
        total_collected=random.randint(8000, 15000),
        segregation_rate=f"{random.randint(75, 95)}%",
        overflow_events=random.randint(0, 15),
        top_waste_types=random.sample(waste_types, k=3)
    )

@app.post("/api/v1/analytics/forecast", response_model=ForecastResponse)
async def get_waste_forecast(request: ForecastRequest):
    """
    Get simulated waste tonnage forecast.
    Returns mock predictions for the next N days.
    """
    dates = []
    predicted_tonnage = []
    confidence_intervals = []
    
    today = datetime.utcnow()
    for i in range(request.days):
        date = today + timedelta(days=i)
        dates.append(date.strftime("%Y-%m-%d"))
        
        # Base tonnage with some variation
        base_tonnage = random.uniform(100, 300)
        tonnage = base_tonnage + (50 * random.uniform(-1, 1))
        predicted_tonnage.append(round(tonnage, 2))
        
        # Confidence interval
        lower_bound = max(0, tonnage * random.uniform(0.85, 0.95))
        upper_bound = tonnage * random.uniform(1.05, 1.15)
        confidence_intervals.append({
            "lower": round(lower_bound, 2),
            "upper": round(upper_bound, 2)
        })
    
    return ForecastResponse(
        dates=dates,
        predicted_tonnage=predicted_tonnage,
        confidence_intervals=confidence_intervals
    )

# ROUTE OPTIMIZATION ENDPOINT
@app.post("/api/v1/routes/optimize", response_model=RouteOptimizeResponse)
async def optimize_routes(request: RouteOptimizeRequest):
    """
    Simulate route optimization for waste collection.
    Returns an ordered list of stops and optimization metrics.
    """
    # Shuffle the locations to simulate optimization
    optimized_route = request.locations.copy()
    random.shuffle(optimized_route)
    
    return RouteOptimizeResponse(
        route_order=optimized_route,
        total_distance=round(random.uniform(50, 200), 2),
        estimated_time=f"{random.randint(2, 8)} hours",
        optimizer_score=round(random.uniform(0.8, 0.99), 3)
    )

# LOGS ENDPOINT
@app.get("/api/v1/logs", response_model=List[LogEntry])
async def get_system_logs(limit: int = 50):
    """
    Get simulated system logs.
    Returns a list of mock log entries.
    """
    log_levels = ["INFO", "WARNING", "ERROR"]
    modules = ["auth", "inference", "cctv", "analytics", "routes", "database", "api", "collection", "vehicle"]
    messages = [
        "User logged in successfully",
        "Image classification completed",
        "CCTV processing job started",
        "Analytics data updated",
        "Route optimization completed",
        "Database connection established",
        "API request processed",
        "Overflow detected at location",
        "New industrial listing added",
        "Forecast model updated",
        "Waste collection completed",
        "Vehicle maintenance scheduled",
        "Report generation completed",
        "Notification sent to user",
        "System backup completed"
    ]
    
    logs = []
    base_time = datetime.utcnow() - timedelta(hours=24)
    
    for i in range(min(limit, 50)):
        log_time = base_time + timedelta(minutes=i*30)
        
        logs.append(LogEntry(
            timestamp=log_time.isoformat() + "Z",
            level=random.choice(log_levels),
            message=random.choice(messages),
            module=random.choice(modules)
        ))
    
    # Sort by timestamp descending (newest first)
    logs.sort(key=lambda x: x.timestamp, reverse=True)
    return logs

# NEW ENDPOINTS FOR EXPANDED FUNCTIONALITY

# Waste Collection Management
@app.post("/api/v1/collections", response_model=WasteCollectionResponse)
async def create_waste_collection(request: WasteCollectionRequest):
    """
    Create a new waste collection record.
    """
    waste_types = ["organic", "plastic", "metal", "glass", "paper"]
    breakdown = {}
    total = 0
    for wt in waste_types:
        amount = round(random.uniform(100, 1000), 2)
        breakdown[wt] = amount
        total += amount
    
    collection = {
        "collection_id": generate_job_id(),
        "ward": request.ward,
        "date": request.date,
        "total_weight": round(total, 2),
        "waste_breakdown": breakdown,
        "collector": fake.name(),
        "status": "completed"
    }
    
    mock_collections.append(collection)
    return WasteCollectionResponse(**collection)

@app.get("/api/v1/collections", response_model=List[WasteCollectionResponse])
async def list_waste_collections(skip: int = 0, limit: int = 20):
    """
    List waste collection records.
    """
    return [WasteCollectionResponse(**collection) for collection in mock_collections[skip:skip+limit]]

@app.get("/api/v1/collections/{collection_id}", response_model=WasteCollectionResponse)
async def get_waste_collection(collection_id: str):
    """
    Get a specific waste collection record.
    """
    for collection in mock_collections:
        if collection["collection_id"] == collection_id:
            return WasteCollectionResponse(**collection)
    raise HTTPException(status_code=404, detail="Collection not found")

# Vehicle Tracking
@app.get("/api/v1/vehicles", response_model=List[VehicleTrackingResponse])
async def list_vehicles():
    """
    List all vehicles with their current status.
    """
    # Update vehicle data to simulate real-time changes
    for vehicle in mock_vehicles:
        # Randomly update some vehicle data
        if random.random() > 0.7:  # 30% chance to update
            vehicle["location"] = {
                "lat": round(random.uniform(12.9, 13.1), 6),
                "lng": round(random.uniform(77.5, 77.7), 6)
            }
            vehicle["status"] = random.choice(["active", "idle", "maintenance"])
            vehicle["last_updated"] = datetime.now().isoformat() + "Z"
            vehicle["route_progress"] = min(100, vehicle["route_progress"] + random.uniform(0, 10))
    
    return [VehicleTrackingResponse(**vehicle) for vehicle in mock_vehicles]

@app.get("/api/v1/vehicles/{vehicle_id}", response_model=VehicleTrackingResponse)
async def get_vehicle(vehicle_id: str):
    """
    Get a specific vehicle's current status.
    """
    for vehicle in mock_vehicles:
        if vehicle["vehicle_id"] == vehicle_id:
            # Update vehicle data
            vehicle["location"] = {
                "lat": round(random.uniform(12.9, 13.1), 6),
                "lng": round(random.uniform(77.5, 77.7), 6)
            }
            vehicle["last_updated"] = datetime.now().isoformat() + "Z"
            return VehicleTrackingResponse(**vehicle)
    raise HTTPException(status_code=404, detail="Vehicle not found")

# User Management
@app.get("/api/v1/users", response_model=UserManagementResponse)
async def list_users():
    """
    List all users in the system.
    """
    active_users = [user for user in mock_users if user["status"] == "active"]
    return UserManagementResponse(
        users=mock_users,
        total_count=len(mock_users),
        active_count=len(active_users)
    )

# Report Generation
@app.post("/api/v1/reports/generate", response_model=ReportGenerationResponse)
async def generate_report(request: ReportGenerationRequest):
    """
    Generate a report of the specified type.
    """
    report_id = generate_job_id()
    
    # Generate mock report data based on type
    report_data = {}
    if request.report_type == "waste_collection":
        report_data = {
            "total_collections": len(mock_collections),
            "total_waste_collected": sum(c["total_weight"] for c in mock_collections),
            "average_per_collection": sum(c["total_weight"] for c in mock_collections) / len(mock_collections) if mock_collections else 0,
            "top_waste_types": ["organic", "plastic", "metal"]
        }
    elif request.report_type == "vehicle_usage":
        report_data = {
            "total_vehicles": len(mock_vehicles),
            "active_vehicles": len([v for v in mock_vehicles if v["status"] == "active"]),
            "total_distance_covered": sum(v["route_progress"] for v in mock_vehicles),
            "utilization_rate": f"{random.randint(70, 95)}%"
        }
    else:
        report_data = {
            "generic_data": "This is a generic report",
            "generated_at": datetime.now().isoformat() + "Z"
        }
    
    report = {
        "report_id": report_id,
        "report_type": request.report_type,
        "generated_at": datetime.now().isoformat() + "Z",
        "data": report_data
    }
    
    mock_reports.append(report)
    return ReportGenerationResponse(**report)

# Notifications
@app.get("/api/v1/notifications", response_model=List[NotificationResponse])
async def list_notifications(unread_only: bool = False):
    """
    List all notifications.
    """
    if unread_only:
        return [NotificationResponse(**n) for n in mock_notifications if not n["read"]]
    return [NotificationResponse(**n) for n in mock_notifications]

@app.post("/api/v1/notifications/{notification_id}/read")
async def mark_notification_read(notification_id: str):
    """
    Mark a notification as read.
    """
    for notification in mock_notifications:
        if notification["id"] == notification_id:
            notification["read"] = True
            return {"status": "success"}
    raise HTTPException(status_code=404, detail="Notification not found")

# Dashboard Metrics
@app.get("/api/v1/dashboard/metrics", response_model=DashboardMetricsResponse)
async def get_dashboard_metrics():
    """
    Get key metrics for the dashboard.
    """
    total_waste = sum(c["total_weight"] for c in mock_collections)
    recycling_rate = round(random.uniform(70, 90), 2)
    co2_saved = round(total_waste * random.uniform(0.5, 1.5), 2)  # kg of CO2 saved
    active_wards = len(set(c["ward"] for c in mock_collections))
    alerts = len([n for n in mock_notifications if not n["read"] and n["type"] == "alert"])
    
    return DashboardMetricsResponse(
        total_waste_collected=total_waste,
        recycling_rate=recycling_rate,
        co2_saved=co2_saved,
        active_wards=active_wards,
        alerts=alerts
    )

# Root endpoint
@app.get("/")
async def root():
    return {"message": "WasteIQ Simulated Backend is running!", 
            "docs": "http://127.0.0.1:8000/docs"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)