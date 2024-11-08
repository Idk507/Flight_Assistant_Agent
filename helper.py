import requests 
from datetime import datetime, timedelta
import json 
import pytz 
import os 

AEROAPI_BASE_URL = "https://aeroapi.flightaware.com/aeroapi"
AEROAPI_KEY = ""  # Make sure to set your API key

# Helper functions
def get_api_session():
    """Create and return an API session with authentication headers."""
    session = requests.Session()
    session.headers.update({"x-apikey": AEROAPI_KEY})
    return session

def fetch_flight_data(flight_id, session):
    """Fetch flight data from the FlightAware API."""
    start_date = datetime.now().date().strftime("%Y-%m-%d")
    end_date = (datetime.now() + timedelta(days=7)).date().strftime("%Y-%m-%d")
    api_resource = f"/flights/{flight_id}?start={start_date}&end={end_date}"
    
    try:
        response = session.get(f"{AEROAPI_BASE_URL}{api_resource}")
        response.raise_for_status()
        return response.json()['flights'][0]
    except requests.exceptions.RequestException as e:
        raise Exception(f"Error fetching flight data: {str(e)}")

def utc_to_local_time(utc_date_str, local_timezone_str):
    """Convert UTC time string to local timezone."""
    try:
        utc_datetime = datetime.strptime(utc_date_str, "%Y-%m-%dT%H:%M:%SZ")
        utc_datetime = utc_datetime.replace(tzinfo=pytz.UTC)
        local_timezone = pytz.timezone(local_timezone_str)
        local_date = utc_datetime.astimezone(local_timezone)
        return local_date.strftime("%Y-%m-%d %H:%M:%S")
    except ValueError as e:
        raise Exception(f"Error converting timezone: {str(e)}")

def get_flight_status(flight_id):
    """Return flight information including status, times, and locations."""
    if not AEROAPI_KEY:
        raise ValueError("FlightAware API key is not set")
    
    try:
        session = get_api_session()
        flight_data = fetch_flight_data(flight_id, session)
        
        # Determine the most accurate departure time
        dept_keys = ["estimated_out", "actual_out", "scheduled_out"]
        dept_key = next((key for key in dept_keys if key in flight_data and flight_data[key]), None)
        
        # Determine the most accurate arrival time
        arr_keys = ["estimated_in", "actual_in", "scheduled_in"]
        arr_key = next((key for key in arr_keys if key in flight_data and flight_data[key]), None)
        
        if not dept_key or not arr_key:
            raise ValueError("Could not find valid departure or arrival times")
        
        flight_details = {
            "source": flight_data["origin"]["city"],
            "destination": flight_data["destination"]["city"],
            "depart_time": utc_to_local_time(flight_data[dept_key], flight_data["origin"]["timezone"]),
            "arrival_time": utc_to_local_time(flight_data[arr_key], flight_data["destination"]["timezone"]),
            "status": flight_data.get("status", "Unknown")
        }
        
        return (f"The current status of flight {flight_id} from {flight_details['source']} to "
                f"{flight_details['destination']} is {flight_details['status']}. "
                f"The flight is scheduled to depart at {flight_details['depart_time']} "
                f"and arrive at {flight_details['arrival_time']}.")
    
    except Exception as e:
        return f"Error retrieving flight status: {str(e)}"

def get_departure_gate(flight_id):
    """Get departure gate information for a flight."""
    # This is a placeholder - implement actual gate retrieval logic
    return "B11"
