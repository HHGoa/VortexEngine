import requests

def get_data_from_api(endpoint, ApiKey, PrivateKey, Address, Chain):
    url = f"https://example.com/api/{endpoint}"  # Replace with the actual API URL
    headers = {
        'Authorization': f'Bearer {ApiKey}',
        'Content-Type': 'application/json'
    }
    params = {
        'private_key': PrivateKey,
        'address': Address,
        'chain': Chain
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()
