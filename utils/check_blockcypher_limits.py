import os
import requests
import json

# Load BlockCypher token from environment variables
token = os.getenv('BLOCKCYPHER_TOKEN')

def check_limits():
    # Send a GET request to the BlockCypher API
    response = requests.get(f"https://api.blockcypher.com/v1/tokens/{token}")

    # Raise an exception if the request was unsuccessful
    response.raise_for_status()

    # Parse the JSON response
    data = response.json()

    # Print the current usage and limits
    print(f"Token: {data['token']}")
    print("Limits:")
    for key, value in data['limits'].items():
        print(f"  {key}: {value}")
    print("Current usage:")
    for key, value in data['hits'].items():
        print(f"  {key}: {value}")
    print("Usage history:")
    for item in data['hits_history']:
        print(f"  Time: {item['time']}")
        for key, value in item.items():
            if key != 'time':
                print(f"    {key}: {value}")

    # Return a boolean indicating whether the usage is OK or not
    return data['hits']['total_hits'] <= data['limits']['total_limits']

if __name__ == '__main__':
    check_limits()
import os
import requests
import json

# Load BlockCypher token from environment variables
token = os.getenv('BLOCKCYPHER_TOKEN')

def check_limits():
    # Send a GET request to the BlockCypher API
    response = requests.get(f"https://api.blockcypher.com/v1/tokens/{token}")

    # Raise an exception if the request was unsuccessful
    response.raise_for_status()

    # Parse the JSON response
    data = response.json()

    # Print the current usage and limits
    print(f"Token: {data['token']}")
    print("Limits:")
    for key, value in data['limits'].items():
        print(f"  {key}: {value}")
    print("Current usage:")
    for key, value in data['hits'].items():
        print(f"  {key}: {value}")
    print("Usage history:")
    for item in data['hits_history']:
        print(f"  Time: {item['time']}")
        for key, value in item.items():
            if key != 'time':
                print(f"    {key}: {value}")

if __name__ == '__main__':
    check_limits()
