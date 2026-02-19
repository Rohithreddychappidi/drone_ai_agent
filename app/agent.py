import re
from .assignment_engine import (
    assign_mission,
    urgent_reassignment,
    get_available_pilots,
    calculate_pilot_cost
)
from .data_layer import load_missions, load_pilots, save_pilots


def handle_query(query: str):
    query = query.lower().strip()

    # ===============================
    # 1. Greeting
    # ===============================
    if any(word in query for word in ["hi", "hello", "hey"]):
        return {
            "message": "Hello 👋 I am your Drone Operations AI Agent. How can I assist you?",
            "examples": [
                "Find pilot for PRJ001",
                "Show available pilots in Mumbai",
                "Urgent assign PRJ002",
                "Calculate cost for Arjun from 2026-02-06 to 2026-02-08",
                "Mark Arjun unavailable"
            ]
        }

    # ===============================
    # 2. Mission Assignment
    # ===============================
    mission_match = re.search(r"prj\d+", query)
    if mission_match:
        mission_id = mission_match.group().upper()

        if "urgent" in query:
            return urgent_reassignment(mission_id)

        if any(word in query for word in ["assign", "find", "handle"]):
            return assign_mission(mission_id)

    # ===============================
    # 3. Show Available Pilots
    # ===============================
    if "available pilots" in query or "show pilots" in query:
        if "mumbai" in query:
            return get_available_pilots(location="Mumbai")
        if "bangalore" in query:
            return get_available_pilots(location="Bangalore")
        return get_available_pilots()

    # ===============================
    # 4. Cost Calculation
    # ===============================
    if "cost" in query:
        name_match = re.search(r"for (\w+)", query)
        date_match = re.findall(r"\d{4}-\d{2}-\d{2}", query)

        if name_match and len(date_match) == 2:
            name = name_match.group(1).capitalize()
            return calculate_pilot_cost(name, date_match[0], date_match[1])

    # ===============================
    # 5. Update Pilot Status
    # ===============================
    if "mark" in query or "set" in query:
        name_match = re.search(r"(arjun|neha|rohit|sneha)", query)
        if name_match:
            name = name_match.group(1).capitalize()
            pilots = load_pilots()

            if "available" in query:
                status = "Available"
            elif "unavailable" in query:
                status = "Unavailable"
            elif "leave" in query:
                status = "On Leave"
            else:
                return {"message": "Please specify status (Available / On Leave / Unavailable)."}

            pilots.loc[pilots["name"] == name, "status"] = status
            save_pilots(pilots)

            return {"message": f"{name} status updated to {status}"}

    # ===============================
    # 6. Show Missions
    # ===============================
    if "missions" in query:
        return load_missions().to_dict(orient="records")

    # ===============================
    # Fallback
    # ===============================
    return {
        "message": "I did not understand your request.",
        "examples": [
            "Find pilot for PRJ001",
            "Show available pilots in Mumbai",
            "Urgent assign PRJ002",
            "Calculate cost for Arjun from 2026-02-06 to 2026-02-08",
            "Mark Arjun unavailable"
        ]
    }
