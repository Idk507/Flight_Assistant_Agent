def setup_gemini():
    """Setup and return Gemini model with tools."""
    try:
        import google.generativeai as genai
        
        tools = [
            {
                "function": get_flight_status,
                "description": "Get flight status information"
            },
            {
                "function": get_departure_gate,
                "description": "Get departure gate information"
            }
        ]
        
        model = genai.GenerativeModel(
            model_name="gemini-pro",
            generation_config={"temperature": 0.3}
        )
        
        return model.start_chat(
            enable_automatic_function_calling=True,
            history=["Hello, what is the status of flight EK226?"]
        )
    except ImportError:
        raise ImportError("Please install the 'google-generativeai' package")

def calculate_layover(first_flight_id, second_flight_id):
    """Calculate layover time between two flights."""
    try:
        session = get_api_session()
        first_flight = fetch_flight_data(first_flight_id, session)
        second_flight = fetch_flight_data(second_flight_id, session)
        
        # Get arrival time of first flight
        arr_key = next((k for k in ["estimated_in", "actual_in", "scheduled_in"] 
                       if k in first_flight and first_flight[k]), None)
        # Get departure time of second flight
        dept_key = next((k for k in ["estimated_out", "actual_out", "scheduled_out"] 
                        if k in second_flight and second_flight[k]), None)
        
        if not arr_key or not dept_key:
            raise ValueError("Could not find valid arrival or departure times")
            
        arrival = datetime.strptime(first_flight[arr_key], "%Y-%m-%dT%H:%M:%SZ")
        departure = datetime.strptime(second_flight[dept_key], "%Y-%m-%dT%H:%M:%SZ")
        
        layover = departure - arrival
        return str(layover)
    except Exception as e:
        return f"Error calculating layover: {str(e)}"
