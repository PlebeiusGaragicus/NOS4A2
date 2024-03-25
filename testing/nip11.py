import requests

url = "https://relay.damus.io/"

# Customize the headers
headers = {
    "Accept": "application/nostr+json",
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Allow-Methods": "GET"
}

# Send a GET request
response = requests.get(url, headers=headers)

# Print the status code
print("Status code: ", response.status_code)

# If the request succeeded, print the data
if response.status_code == 200:
    print("Data: ", response.json())
else:
    print("Request failed.")
