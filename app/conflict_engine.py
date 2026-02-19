from datetime import datetime

def date_overlap(start1, end1, start2, end2):
    return start1 <= end2 and start2 <= end1


def skill_mismatch(pilot_skills, required_skill):
    return required_skill.lower() not in pilot_skills.lower()


def certification_mismatch(pilot_certs, required_certs):
    required = [c.strip() for c in required_certs.split(",")]
    pilot = [c.strip() for c in pilot_certs.split(",")]
    return not all(cert in pilot for cert in required)


def weather_conflict(drone_weather_resistance, mission_weather):
    if mission_weather == "Rainy" and "IP43" not in drone_weather_resistance:
        return True
    return False
