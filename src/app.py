"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports p",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Basketball Team": {
        "description": "Team practices and competitive basketball games",
        "schedule": "Mondays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 15,
        "participants": ["alex@mergington.edu", "mia@mergington.edu"]
    },
    "Swimming Club": {
        "description": "Swim training and water safety for all levels",
        "schedule": "Tuesdays and Fridays, 3:45 PM - 5:15 PM",
        "max_participants": 18,
        "participants": ["nina@mergington.edu", "ryan@mergington.edu"]
    },
    "Art Workshop": {
        "description": "Explore drawing, painting, and mixed media art projects",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 16,
        "participants": ["sara@mergington.edu", "leo@mergington.edu"]
    },
    "Drama Club": {
        "description": "Rehearse and perform plays, scenes, and improvisations",
        "schedule": "Thursdays, 4:00 PM - 6:00 PM",
        "max_participants": 20,
        "participants": ["isabel@mergington.edu", "mason@mergington.edu"]
    },
    "Science Club": {
        "description": "Investigate scientific principles with experiments and projects",
        "schedule": "Mondays, 4:00 PM - 5:00 PM",
        "max_participants": 14,
        "participants": ["nora@mergington.edu", "ethan@mergington.edu"]
    },
    "Debate Team": {
        "description": "Practice public speaking and competitive debate tournaments",
        "schedule": "Wednesdays and Fridays, 4:30 PM - 6:00 PM",
        "max_participants": 12,
        "participants": ["zoe@mergington.edu", "matt@mergington.edu"]
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Normalize and validate email
    normalized = email.strip().lower()
    if normalized in [e.strip().lower() for e in activity.get("participants", [])]:
        raise HTTPException(status_code=400, detail="Student already signed up")

    # Check capacity
    if len(activity.get("participants", [])) >= activity.get("max_participants", 0):
        raise HTTPException(status_code=400, detail="Activity is full")

    # Add student
    activity.setdefault("participants", []).append(normalized)
    return {"message": f"Signed up {normalized} for {activity_name}"}


@app.delete("/activities/{activity_name}/participants")
def remove_participant(activity_name: str, email: str):
    """Unregister a student from an activity"""
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    activity = activities[activity_name]
    normalized = email.strip().lower()
    participants = activity.get("participants", [])
    normalized_list = [e.strip().lower() for e in participants]
    if normalized not in normalized_list:
        raise HTTPException(status_code=404, detail="Participant not found")

    # remove the original entry preserving casing if any
    idx = normalized_list.index(normalized)
    participants.pop(idx)
    return {"message": f"Removed {normalized} from {activity_name}"}
