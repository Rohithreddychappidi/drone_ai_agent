<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/c51a060f-b4aa-4b42-89ba-6e60878d83a2" />


# 🚁 Skylark Drones – Drone Operations Coordinator AI Agent

An AI-powered coordination system designed to automate pilot assignment, drone allocation, conflict detection, and urgent mission handling for multi-project drone operations.

This project was developed as part of the Skylark Drones Technical Assignment.

---

## 📌 Problem Overview

Skylark Drones manages multiple drone missions simultaneously across different locations.

Traditionally, a human coordinator handles:

* Pilot availability tracking
* Mission-to-pilot matching
* Drone inventory monitoring
* Conflict detection
* Urgent reassignment coordination

This system replaces manual coordination with a structured AI-driven decision engine.

---

## 🎯 Objective

Build a conversational AI agent capable of:

* Managing pilot rosters
* Matching pilots to missions
* Matching drones based on weather compatibility
* Detecting operational conflicts
* Handling urgent reassignment logic
* Syncing updates with Google Sheets (2-way integration)

---

# 🏗️ Architecture Overview

```
drone_ai_agent/
│
├── app/
│   ├── main.py                # FastAPI entry point
│   ├── agent.py               # Conversational routing logic
│   ├── assignment_engine.py   # Pilot & drone matching logic
│   ├── conflict_engine.py     # Conflict validation rules
│   ├── data_layer.py          # Data loading & sheet sync
│
├── templates/
│   └── index.html             # Chatbot frontend UI
│
├── requirements.txt
├── README.md
```

---

# ⚙️ Tech Stack

### Backend

* **FastAPI** – REST API & conversational interface
* **Pandas** – Rule-based evaluation engine
* **Google Sheets API (gspread)** – Lightweight cloud database
* **Uvicorn** – ASGI server

### Frontend

* HTML + TailwindCSS
* Simple conversational UI

### Deployment

* Hosted on **Render (Free Tier)**

---

# 🔄 System Flow

### Example Interaction:

**User:**

> "Find pilot for PRJ001"

**Agent Logic:**

1. Reads live data from Google Sheets
2. Checks:

   * Skill match
   * Certification match
   * Location match
   * Budget constraint
   * Weather compatibility
3. Returns eligible pilot(s) and drone(s)

**Optional:**
If confirmed → system updates pilot status in Google Sheets.

---

# 🧠 Core Features

## 1️⃣ Pilot Roster Management

* Query available pilots
* Filter by skill and location
* Calculate mission cost
* Update pilot status (syncs to Google Sheets)

---

## 2️⃣ Assignment Engine

* Match pilot to mission
* Match drone to mission
* Budget validation
* Weather compatibility filtering

---

## 3️⃣ Drone Inventory

* Filter by capability
* Filter by weather resistance
* Maintenance validation
* Location-based filtering

---

## 4️⃣ Conflict Detection

The system detects:

* Skill mismatch
* Certification mismatch
* Budget overrun
* Weather incompatibility
* Location mismatch
* Maintenance conflicts

---

## 🚨 Urgent Reassignment Logic

If a mission is marked **High** or **Urgent**:

* System prioritizes assignment
* If no eligible pilot available:

  * Suggests reassignment from lower-priority missions
  * Flags for manual review

No automatic override occurs without confirmation.

---

# 🔗 Google Sheets Integration

This system uses Google Sheets as a live database.

### Two-Way Sync:

* Reads: Pilot roster & drone fleet
* Writes: Pilot status updates

This allows:

* Real-time coordination
* Non-technical stakeholder visibility
* Lightweight cloud storage

---

# 🚀 Deployment

The project is deployed on Render.

To run locally:

```bash
# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Run server
uvicorn app.main:app --reload
```

Access:

```
http://127.0.0.1:8000
```

API Docs:

```
http://127.0.0.1:8000/docs
```

---

# 🧪 Sample API Endpoints

### Assign Mission

```
POST /assign/PRJ001
```

### Urgent Assignment

```
POST /urgent_assign/PRJ002
```

### Get Available Pilots

```
GET /pilots
```

### Calculate Pilot Cost

```
GET /pilot_cost?name=Arjun&start=2026-02-06&end=2026-02-08
```

### Update Pilot Status

```
POST /update_pilot_status?name=Arjun&status=Unavailable
```

---

# 📈 Design Philosophy

This solution intentionally uses:

* Deterministic rule-based decision logic
* Modular architecture
* Clear conflict validation
* Transparent operational flow

Rather than integrating heavy LLM frameworks, the focus was on building a reliable, explainable operational coordination system within the 6-hour constraint.

---

# 🔮 Future Improvements

If extended further, the system could include:

* Date overlap detection across missions
* Travel time estimation
* Weather API integration
* Multi-pilot missions
* AI-based ranking of pilot-drone combinations
* PostgreSQL database integration

---

# 👨‍💻 Author

Developed as part of Skylark Drones Technical Assignment.

---
