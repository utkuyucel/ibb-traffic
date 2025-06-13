import requests
from typing import List, Dict, Any
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

@dataclass
class ApiResponse:
    status_code: int
    data: List[Dict[str, Any]]
    message: str = None
    

class ApiClient:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def get(self, endpoint: str, params: Dict[str, Any] = None) -> ApiResponse:
        response = requests.get(f"{self.base_url}/{endpoint}", params=params)
        return self._handle_response(response)

    def post(self, endpoint: str, data: Dict[str, Any]) -> ApiResponse:
        response = requests.post(f"{self.base_url}/{endpoint}", json=data)
        return self._handle_response(response)

    def _handle_response(self, response: requests.Response) -> ApiResponse:
        if response.ok:
            logger.info("API request successful.")
            return ApiResponse(status_code=response.status_code, data=response.json())
        else:
            logger.error("API request failed.")
            return ApiResponse(status_code=response.status_code, data=[], message=response.text)


if __name__ == "__main__":
    URL = "https://tkmservices.ibb.gov.tr/web/api/TrafficData/v1"
    client = ApiClient(base_url=URL)
    response = client.get("/TrafficIndex_Sc1_Cont")

    print("Response from API:")
    print(f"Status code: {response.status_code}")
    print(f"Data:{response.data}")
    print(f"Message:{response.message}")


