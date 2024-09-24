from rest_framework.response import Response
from .utils import get_active_mac_ip
import requests
from rest_framework.decorators import api_view
import json
from .models import Keys
from UserController.models import CustomUser

@api_view(['GET'])
def get_mac_ip_view(request):
    mac_ip_data = get_active_mac_ip()
    return Response(mac_ip_data, status=200)

@api_view(['POST'])
def good(request):
    data = '''{
  "name": "example_name",
  "license_key": "example_license_key",
  "license_type": "example_license_type",
  "license_status": "active",
  "license_expiry": "2025-09-25",
  "connection_limit": 5,
  "payment_system": "example_payment_system",
  "mac_address": "00:1A:2B:3C:4D:5E",
  "ip_address": "192.168.0.1"
}
'''
    encode = json.loads(data)
    return Response(encode, status=200)

@api_view(['POST'])
def activate_license(request):
    # Get MAC and IP addresses
    data = get_active_mac_ip()
    mac_address_list = [entry['mac_address'] for entry in data]
    ip_address_list = [entry['ip_address'] for entry in data]

    # Prepare the payload for the request
    payload = {
        "mac_address_list": mac_address_list,
        "ip_address_list": ip_address_list
    }

    # The external API endpoint
    url = "http://192.168.9.31:8000/license/good/"

    try:
        # Send the POST request to the external API
        response = requests.post(url, json=payload)
        response.raise_for_status()  # Raise an error if the status code is 4xx or 5xx
        response_data = response.json()
        Keys.objects.create(
            name=response_data.get('name'),
            license_key=response_data.get('license_key'),
            license_type=response_data.get('license_type'),
            license_status=response_data.get('license_status'),
            license_expiry=response_data.get('license_expiry'),
            connection_limit=response_data.get('connection_limit'),
            payment_system=response_data.get('payment_system'),
            mac_address=response_data.get('mac_address'),
            ip_address=response_data.get('ip_address')
        )

        # Return the external API response to the client
        return Response(response_data, status=response.status_code)

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        return Response({"error": "Failed to activate license: HTTP error"}, status=500)

    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error occurred: {conn_err}")
        return Response({"error": "Failed to connect to external API"}, status=500)

    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout error occurred: {timeout_err}")
        return Response({"error": "Request to external API timed out"}, status=500)

    except requests.exceptions.RequestException as req_err:
        print(f"An error occurred: {req_err}")
        return Response({"error": "An error occurred while sending request"}, status=500)
