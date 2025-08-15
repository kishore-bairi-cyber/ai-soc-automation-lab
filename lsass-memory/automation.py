
# Placeholder: SentinelOne API call to isolate host
import requests

def isolate_host(device_id, token):
    url = f"https://api.sentinelone.com/devices/{device_id}/actions/isolate"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(url, headers=headers)
    return response.status_code, response.json()
