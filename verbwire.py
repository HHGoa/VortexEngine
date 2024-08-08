import requests
import json
import io
import uuid

def upload_json_as_file(json_text):
    # Generate a unique filename using UUID
    filename = f"{uuid.uuid4()}.json"
    
    # Convert the input JSON text to a Python dictionary
    json_data = json.loads(json_text)
    
    # Convert the JSON data to bytes for the file-like object
    json_bytes = json.dumps(json_data).encode('utf-8')
    json_file_like = io.BytesIO(json_bytes)
    
    # Define the API endpoint and the necessary headers
    url = "https://api.verbwire.com/v1/nft/store/file"
    files = { "filePath": (filename, json_file_like, "application/json") }
    headers = {
        "accept": "application/json",
        "X-API-Key": "sk_live_0c7597d2-dd10-44c5-8488-fd60859c61f1"
    }
    
    # Send the POST request with the file-like JSON object
    response = requests.post(url, files=files, headers=headers)
    
    # Return the server response
    return response.text

# Sample JSON text
sample_json_text = '{"name": "example", "description": "This is a test JSON."}'

# Call the function and print the response
response_text = upload_json_as_file(sample_json_text)
print(response_text)
