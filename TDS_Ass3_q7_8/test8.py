from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import re
import json

# Define the pre-templatized functions (placeholders for this task)
def get_ticket_status(ticket_id: int):
    return {"status": "Open"}  # Sample return value

def schedule_meeting(date: str, time: str, meeting_room: str):
    return {"status": "Scheduled", "meeting_details": {"date": date, "time": time, "room": meeting_room}}

def get_expense_balance(employee_id: int):
    return {"balance": 500.75}  # Sample balance

def calculate_performance_bonus(employee_id: int, current_year: int):
    return {"bonus": 1200.50}  # Sample bonus

def report_office_issue(issue_code: int, department: str):
    return {"status": "Reported", "issue_code": issue_code, "department": department}

# Initialize FastAPI app
app = FastAPI()

# Enable CORS for all origins and specific methods
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["OPTIONS", "GET"],
    allow_headers=["*"],
)

# Define the /execute endpoint
@app.get("/execute")
async def execute_task(q: str):
    # Match ticket status query
    match_ticket_status = re.match(r"What is the status of ticket (\d+)\?", q)
    if match_ticket_status:
        ticket_id = int(match_ticket_status.group(1))
        return {"name": "get_ticket_status", "arguments": json.dumps({"ticket_id": ticket_id}, separators=(",", ":"))}

    # Match meeting scheduling query
    match_schedule_meeting = re.match(r"Schedule a meeting on (\d{4}-\d{2}-\d{2}) at (\d{2}:\d{2}) in (.+)\.", q)
    if match_schedule_meeting:
        date = match_schedule_meeting.group(1)
        time = match_schedule_meeting.group(2)
        meeting_room = match_schedule_meeting.group(3)
        return {"name": "schedule_meeting", "arguments": json.dumps({"date": date, "time": time, "meeting_room": meeting_room}, separators=(",", ":"))}

    # Match expense balance query
    match_expense_balance = re.match(r"Show my expense balance for employee (\d+)\.", q)
    if match_expense_balance:
        employee_id = int(match_expense_balance.group(1))
        return {"name": "get_expense_balance", "arguments": json.dumps({"employee_id": employee_id}, separators=(",", ":"))}

    # Match performance bonus query (more flexible wording)
    match_performance_bonus = re.match(r"(?:Calculate|Fetch) (?:performance )?bonus for (?:employee|emp) (\d+) for (\d{4})", q)
    if match_performance_bonus:
        employee_id = int(match_performance_bonus.group(1))
        current_year = int(match_performance_bonus.group(2))
        return {"name": "calculate_performance_bonus", "arguments": json.dumps({"employee_id": employee_id, "current_year": current_year}, separators=(",", ":"))}

    # Match office issue reporting query
    match_office_issue = re.match(r"Report office issue (\d+) for the (.+) department\.", q)
    if match_office_issue:
        issue_code = int(match_office_issue.group(1))
        department = match_office_issue.group(2)
        return {"name": "report_office_issue", "arguments": json.dumps({"issue_code": issue_code, "department": department}, separators=(",", ":"))}

    # If no match found, raise an exception
    raise HTTPException(status_code=400, detail="Query not recognized.")

# Run the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8080)
