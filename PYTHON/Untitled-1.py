

class testwala:
    def __init__(self,name,salary):
        self.name = name(str("enter a name"))
        self.salary = salary(int("enter a salary"))
        
    def diaplay(self):
        print(self.name)
        print(self.salary)
a = testwala()
a.diaplay()
        

from datetime import datetime
from typing import Dict, Any

class PayloadValidator:
    def __init__(self):
        # Required fields per command type
        self.format = {
            "/schedule_refresh": ["groupId", "datasetId", "reportName", "day", "time"],
        }

    # Evaluated at class definition time (kept as in your original code; not used in validation)
    now = datetime.now()
    day = now.strftime("%A")
    time = now.strftime("%H:%M:%S")

    def validate_payload(self, payload: Dict[str, Any]) -> bool:
        
        # --- Step 1: Validate payload is a dictionary (safety first) ---
        if not isinstance(payload, dict):
            print("Validation failed: Payload must be a dictionary.")
            return False

        # --- Step 2: Validate required fields exist ---
        required_fields = self.format.get("/schedule_refresh", [])
        missing = [key for key in required_fields if key not in payload]
        if missing:
            print(f"Validation failed: Missing required fields: {', '.join(missing)}")
            return False

        # --- Step 3: Validate 'day' format (expect uppercase weekday like 'FRIDAY') ---
        day_val = payload.get('day')
        valid_days = {
            "MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY",
            "FRIDAY", "SATURDAY", "SUNDAY"
        }

        if not isinstance(day_val, str) or day_val.upper() not in valid_days:
            # Show expected format and what was received
            print(f"Invalid date format: {day_val}. Expected format: FRIDAY")
            return False

        # --- Step 4: Validate 'time' format (HH:MM:SS) ---
        time_val = payload.get('time')
        if not isinstance(time_val, str):
            print(f"Invalid time format: {time_val}. Expected format: HH:MM:SS")
            return False

        try:
            # This checks both structure and value ranges (00-23 for hours, 00-59 for minutes/seconds)
            datetime.strptime(time_val, "%H:%M:%S")
        except ValueError:
            print(f"Invalid time format: {time_val}. Expected format: HH:MM:SS")
            return False

        # If all checks succeeded
        print("Validation successful: Date and time formats are valid.")
        return True
