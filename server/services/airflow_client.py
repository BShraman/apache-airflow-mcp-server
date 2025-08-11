import httpx
import requests
from typing import Any
from dotenv import load_dotenv
import os

# Load from environment variables
load_dotenv()

class AirflowClient():
    def __init__(self):
        self.endpoint_url = os.getenv("_END_POINT_UTL", "http://localhost:8080")
        self.username = os.getenv("_AIRFLOW_WWW_USER_USERNAME", "airflow")
        self.password = os.getenv("_AIRFLOW_WWW_USER_PASSWORD", "airflow")

    def generate_jwt_token(self) -> str:
        """Generate JWT token for Airflow REST API authentication."""
        auth_url = f"{self.endpoint_url}/auth/token"

        payload = {
            "username": self.username,
            "password": self.password
        }

        headers = {
            "Content-Type": "application/json"
        }

        response = requests.post(auth_url, json=payload, headers=headers)

        if response.status_code in (200, 201):
            return response.json().get("access_token", "")
        else:
            raise Exception(f"Authentication failed: {response.status_code} {response.text}")

    async def api_request(self, endpoint: str, method: str, **kwargs) -> Any:
        """Make a request to the Airflow API server with JWT authentication."""
        url = f"{self.endpoint_url}/api/v2/{endpoint}"

        try:
            jwt_token = self.generate_jwt_token()
            if not jwt_token:
                raise Exception("Failed to generate JWT token")
            
            headers = {
                "Authorization": f"Bearer {jwt_token}",
                "Accept": "application/json"
            }

            async with httpx.AsyncClient() as client:
                request_method = getattr(client, method.lower(), None)

                if not callable(request_method):
                    raise ValueError(f"Invalid HTTP method: {method}")

                response = await request_method(url, headers=headers, **kwargs)

                if response.status_code == 200:
                    return response.json()
                else:
                    return {
                        "status": response.status_code,
                        "error": response.text
                    }

        except Exception as e:
            print(f"Exception during Airflow API request: {e}")
            return {"error": str(e)}
