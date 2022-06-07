import os
import requests
import json

def decentroAPI(type, id):
    url = "https://in.staging.decentro.tech/kyc/public_registry/validate"

    payload = json.dumps({
    "reference_id": "0000-0000-0000-2004",
    "document_type": type,
    "id_number": id,
    "consent": "Y",
    "consent_purpose": "For bank account purpose only"
    })
    headers = {
    'client_id': os.environ.get('client_id'),
    'client_secret': os.environ.get('client_secret'),
    'module_secret': os.environ.get('module_secret'),
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    result = json.loads(response.text)
    return result