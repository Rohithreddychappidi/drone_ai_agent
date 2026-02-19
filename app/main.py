from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from .assignment_engine import (
    assign_mission,
    urgent_reassignment,
    get_available_pilots,
    calculate_pilot_cost
)
from .agent import handle_query
from .data_layer import load_pilots, save_pilots

app = FastAPI()

# Setup templates folder
templates = Jinja2Templates(directory="templates")


# =========================
# FRONTEND CHAT PAGE
# =========================
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# =========================
# CHAT ENDPOINT
# =========================
@app.post("/chat")
def chat(query: str):
    return handle_query(query)


# =========================
# ASSIGNMENT ENDPOINTS
# =========================
@app.post("/assign/{project_id}")
def assign(project_id: str):
    return assign_mission(project_id)


@app.post("/urgent_assign/{project_id}")
def urgent_assign(project_id: str):
    return urgent_reassignment(project_id)


# =========================
# ROSTER MANAGEMENT
# =========================
@app.get("/pilots")
def available_pilots(skill: str = None, location: str = None):
    return get_available_pilots(skill, location)


@app.get("/pilot_cost")
def pilot_cost(name: str, start: str, end: str):
    return calculate_pilot_cost(name, start, end)


@app.post("/update_pilot_status")
def update_pilot_status(name: str, status: str):
    pilots = load_pilots()

    if name not in pilots["name"].values:
        return {"error": "Pilot not found"}

    pilots.loc[pilots["name"] == name, "status"] = status
    save_pilots(pilots)

    return {"message": f"{name} status updated to {status}"}
