# Flight Status Tracker

A Python application that tracks flight statuses, departure gates, and calculates layover times using FlightAware's AeroAPI, Google's Gemini AI, and LangChain.

## Features

- Real-time flight status tracking
- Departure gate information
- Layover time calculation
- AI-powered flight information retrieval using Gemini
- Advanced query processing using LangChain

## Prerequisites

- Python 3.8 or higher
- FlightAware AeroAPI account
- Google Cloud Platform account (for Gemini AI)

## Getting Started

### 1. Setting up FlightAware AeroAPI

1. Create a FlightAware account:
   - Go to [FlightAware's website](https://flightaware.com/)
   - Click "Sign Up" in the top right corner
   - Complete the registration process

2. Get AeroAPI access:
   - Log into your FlightAware account
   - Visit [AeroAPI Portal](https://flightaware.com/aeroapi/portal/)
   - Click "Create New Application"
   - Fill in your application details:
     - Name: Your application name
     - Description: Brief description of your use case
     - Select the appropriate plan (Free tier available)
   - Submit the application

3. Get your API key:
   - Once approved, go to your AeroAPI Portal
   - Find your application
   - Copy the API key provided

### 2. Setting up Google Cloud Platform for Gemini

1. Create a Google Cloud Project:
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Click "New Project"
   - Enter project details and create

2. Enable the Gemini API:
   - In the Cloud Console, go to "APIs & Services" > "Library"
   - Search for "Generative Language API"
   - Click "Enable"

3. Create API credentials:
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "API Key"
   - Copy the generated API key

### 3. Installation

1. Clone the repository:
```bash
git clone [https://github.com/yourusername/flight-status-tracker.git](https://github.com/Idk507/Flight_Assistant_Agent)
cd flight-status-tracker
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
# On Unix/Linux/macOS
export AEROAPI_KEY="your_flightaware_api_key"
export GOOGLE_API_KEY="your_google_api_key"

# On Windows
set AEROAPI_KEY=your_flightaware_api_key
set GOOGLE_API_KEY=your_google_api_key
```

## Usage

### Basic Flight Status Check
```python
from flight_tracker import get_flight_status

# Get status for a specific flight
status = get_flight_status("EK226")
print(status)
```

### Calculate Layover Time
```python
from flight_tracker import calculate_layover

# Calculate layover between two flights
layover = calculate_layover("EK226", "EK242")
print(f"Layover time: {layover}")
```

### Using AI Features
```python
from flight_tracker import setup_gemini, setup_langchain

# Using Gemini
chat = setup_gemini()
response = chat.send_message("What is the departure gate for flight EK226?")
print(response.text)

# Using LangChain
agent = setup_langchain()
response = agent.invoke({
    "input": "What is the status of EK242?"
})
print(response['output'])
```

## API Response Examples

### Flight Status Response
```json
{
    "source": "Dubai",
    "destination": "Singapore",
    "depart_time": "2024-11-08 14:30:00",
    "arrival_time": "2024-11-09 02:15:00",
    "status": "Scheduled"
}
```

## Error Handling

The application handles various types of errors:
- Invalid API keys
- Network connection issues
- Invalid flight numbers
- Missing flight data
- Timezone conversion errors

Example error handling:
```python
try:
    status = get_flight_status("INVALID")
except Exception as e:
    print(f"Error: {str(e)}")
```

## Best Practices

1. Always check your API key validity before making requests
2. Handle rate limits appropriately
3. Implement error handling for all API calls
4. Keep API keys secure and never commit them to version control
5. Use environment variables for sensitive information

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please:
1. Check the existing issues
2. Create a new issue with detailed information
3. Contact FlightAware support for API-specific issues
4. Contact Google support for Gemini API issues

## Acknowledgments

- FlightAware for providing the AeroAPI
- Google for the Gemini AI API
- LangChain community for their excellent framework
