import logging
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import requests


logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class ApiResponse:
    """Response object for API calls."""

    status_code: int
    data: List[Dict[str, Any]]
    message: Optional[str] = None


class ApiClient:
    """Client for interacting with IBB Traffic Data API."""

    def __init__(self, base_url: str) -> None:
        self.base_url = base_url.rstrip("/")

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> ApiResponse:
        """Make a GET request to the API."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = requests.get(url, params=params)
        return self._handle_response(response)

    def post(self, endpoint: str, data: Dict[str, Any]) -> ApiResponse:
        """Make a POST request to the API."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = requests.post(url, json=data)
        return self._handle_response(response)

    def _handle_response(self, response: requests.Response) -> ApiResponse:
        """Handle API response and create ApiResponse object."""
        if response.ok:
            logger.info("API request successful.")
            try:
                data = response.json()
                if isinstance(data, list):
                    return ApiResponse(status_code=response.status_code, data=data)
                else:
                    return ApiResponse(status_code=response.status_code, data=[data])
            except ValueError:
                logger.warning("Response is not valid JSON")
                return ApiResponse(status_code=response.status_code, data=[])
        else:
            logger.error(f"API request failed with status code {response.status_code}.")
            return ApiResponse(status_code=response.status_code, data=[], message=response.text)


def main() -> None:
    """Example usage of the API client."""
    url = "https://tkmservices.ibb.gov.tr/web/api/TrafficData/v1"
    client = ApiClient(base_url=url)
    response = client.get("/TrafficIndex_Sc1_Cont")

    print("Response from API:")
    print(f"Status code: {response.status_code}")
    print(f"Data: {response.data}")
    print(f"Message: {response.message}")


if __name__ == "__main__":
    main()
