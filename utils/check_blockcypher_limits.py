import os
import dotenv
import requests
import json
from decouple import Config, Csv

# Retrieve the value of BLOCKCYPHER_TOKEN
dotenv.load_dotenv()
assert os.environ.get("BLOCKCYPHER_TOKEN"), "BLOCKCYPHER_TOKEN not found in .env file"
token = os.environ.get("BLOCKCYPHER_TOKEN")

def check_limits():
    try:
        # Send a GET request to the BlockCypher API
        response = requests.get(f"https://api.blockcypher.com/v1/tokens/{token}")

        # Raise an exception if the request was unsuccessful
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
        return False

    # Parse the JSON response
    data = response.json()

    # Check if 'hits_history' key exists in the data dictionary
    if 'hits_history' in data:
        total_hits = 0
        for item in data['hits_history']:
            for key, value in item.items():
                if key == 'api/hour':
                    total_hits += value

        # Return a boolean indicating whether the usage is OK or not
        return total_hits <= data['limits']['api/day']
    else:
        print("Error: 'hits' key not found in the API response. Here is the full response:")
        print(json.dumps(data, indent=4))
        exit(1)
