import pandas as pd
from datetime import datetime
from .data_layer import load_pilots, load_drones, load_missions
from .conflict_engine import (
    skill_mismatch,
    certification_mismatch,
    weather_conflict
)

# ================================
# ROSTER MANAGEMENT
# ================================

def get_available_pilots(skill=None, location=None):
    df = load_pilots()

    df = df[df["status"] == "Available"]

    if skill:
        df = df[df["skills"].str.contains(skill, case=False, na=False)]

    if location:
        df = df[df["location"] == location]

    return df.to_dict(orient="records")


def calculate_pilot_cost(pilot_name, start_date, end_date):
    df = load_pilots()

    pilot = df[df["name"] == pilot_name]

    if pilot.empty:
        return {"error": "Pilot not found"}

    try:
        # Ensure numeric
        cost_per_day = float(pilot.iloc[0]["daily_rate_inr"])

        # Parse dates safely
        start = datetime.strptime(start_date.strip(), "%Y-%m-%d")
        end = datetime.strptime(end_date.strip(), "%Y-%m-%d")

        days = (end - start).days + 1

        if days <= 0:
            return {"error": "Invalid date range"}

        return {"total_cost": cost_per_day * days}

    except Exception as e:
        return {"error": f"Calculation failed: {str(e)}"}

# ================================
# DRONE INVENTORY
# ================================

def get_available_drones(required_capability=None, location=None, weather=None):
    drones = load_drones()

    drones = drones[drones["status"] == "Available"]

    # Maintenance check
    today = datetime.today().date()
    drones["maintenance_due"] = pd.to_datetime(
        drones["maintenance_due"]
    ).dt.date

    drones = drones[drones["maintenance_due"] >= today]

    if required_capability:
        drones = drones[
            drones["capabilities"].str.contains(
                required_capability, case=False, na=False
            )
        ]

    if location:
        drones = drones[drones["location"] == location]

    if weather:
        drones = drones[
            ~drones.apply(
                lambda row: weather == "Rainy"
                and "IP43" not in row["weather_resistance"],
                axis=1
            )
        ]

    return drones.to_dict(orient="records")


# ================================
# FULL ASSIGNMENT ENGINE
# ================================

def assign_mission(project_id):

    pilots = load_pilots()
    drones = load_drones()
    missions = load_missions()

    mission = missions[missions["project_id"] == project_id]

    if mission.empty:
        return {"status": "Error", "message": "Mission not found"}

    mission = mission.iloc[0]

    start = datetime.strptime(mission["start_date"], "%Y-%m-%d")
    end = datetime.strptime(mission["end_date"], "%Y-%m-%d")
    duration_days = (end - start).days + 1

    eligible_pilots = []
    pilot_warnings = []

    # ------------------------
    # PILOT MATCHING
    # ------------------------

    for _, pilot in pilots.iterrows():

        if pilot["status"] != "Available":
            continue

        if pilot["location"] != mission["location"]:
            continue

        if pilot["current_assignment"] != "-":
            pilot_warnings.append(
                f"{pilot['name']} already assigned to {pilot['current_assignment']}"
            )
            continue

        if skill_mismatch(pilot["skills"], mission["required_skills"]):
            continue

        if certification_mismatch(
            pilot["certifications"],
            mission["required_certs"]
        ):
            pilot_warnings.append(
                f"Certification mismatch for {pilot['name']}"
            )
            continue

        total_cost = pilot["daily_rate_inr"] * duration_days

        if total_cost > mission["mission_budget_inr"]:
            pilot_warnings.append(
                f"Budget overrun risk for {pilot['name']}"
            )
            continue

        eligible_pilots.append({
            "pilot_id": pilot["pilot_id"],
            "name": pilot["name"],
            "estimated_cost": total_cost
        })

    # ------------------------
    # DRONE MATCHING
    # ------------------------

    eligible_drones = []
    drone_warnings = []

    for _, drone in drones.iterrows():

        if drone["status"] != "Available":
            continue

        if drone["location"] != mission["location"]:
            continue

        if drone["current_assignment"] != "-":
            drone_warnings.append(
                f"Drone {drone['drone_id']} already deployed"
            )
            continue

        if weather_conflict(
            drone["weather_resistance"],
            mission["weather_forecast"]
        ):
            drone_warnings.append(
                f"Weather risk for drone {drone['drone_id']}"
            )
            continue

        eligible_drones.append(drone["drone_id"])

    return {
        "mission": project_id,
        "eligible_pilots": eligible_pilots,
        "eligible_drones": eligible_drones,
        "pilot_warnings": pilot_warnings,
        "drone_warnings": drone_warnings
    }


# ================================
# URGENT REASSIGNMENT
# ================================

def urgent_reassignment(project_id):

    missions = load_missions()
    mission = missions[missions["project_id"] == project_id]

    if mission.empty:
        return {"status": "Error", "message": "Mission not found"}

    mission = mission.iloc[0]

    if mission["priority"] not in ["High", "Urgent"]:
        return {"message": "Mission is not high priority"}

    result = assign_mission(project_id)

    if result["eligible_pilots"]:
        return result

    return {
        "message": "No direct pilot available. Suggest reassigning from lower priority mission."
    }
