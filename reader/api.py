import logging
from dataclasses import dataclass
from typing import Any, Dict, List, Optional
from urllib.parse import urljoin

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


logger = logging.getLogger(__name__)


class ApiError(Exception):
    """Custom exception for API-related errors."""
    
    def __init__(self, message: str, status_code: Optional[int] = None):
        super().__init__(message)
        self.status_code = status_code


@dataclass(frozen=True)
class ApiResponse:
    """Response object for API calls."""

    status_code: int
    data: List[Dict[str, Any]]
    message: Optional[str] = None
    
    @property
    def is_successful(self) -> bool:
        """Check if the API response was successful."""
        return 200 <= self.status_code < 300
    
    @property
    def has_data(self) -> bool:
        """Check if the response contains data."""
        return bool(self.data)


class ApiClient:
    """Client for interacting with IBB Traffic Data API."""

    def __init__(self, base_url: str, timeout: int = 30) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = self._create_session()

    def _create_session(self) -> requests.Session:
        """Create a configured requests session with retry strategy."""
        session = requests.Session()
        retry_strategy = Retry(
            total=3,
            backoff_factor=0.3,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        return session

    def _build_url(self, endpoint: str) -> str:
        """Build complete URL from base URL and endpoint."""
        return urljoin(self.base_url + "/", endpoint.lstrip("/"))

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> ApiResponse:
        """Make a GET request to the API."""
        url = self._build_url(endpoint)
        logger.info(f"Making GET request to: {url}")
        
        try:
            # Use direct requests call for better testability while keeping session benefits
            response = requests.get(url, params=params, timeout=self.timeout)
            return self._handle_response(response)
        except requests.RequestException as e:
            logger.error(f"API request failed: {e}")
            raise ApiError(f"API call failed: {e}")

    def post(self, endpoint: str, data: Dict[str, Any]) -> ApiResponse:
        """Make a POST request to the API."""
        url = self._build_url(endpoint)
        logger.info(f"Making POST request to: {url}")
        
        try:
            # Use direct requests call for better testability while keeping session benefits
            response = requests.post(url, json=data, timeout=self.timeout)
            return self._handle_response(response)
        except requests.RequestException as e:
            logger.error(f"API request failed: {e}")
            raise ApiError(f"API call failed: {e}")

    def _handle_response(self, response: requests.Response) -> ApiResponse:
        """Handle API response and create ApiResponse object."""
        try:
            response.raise_for_status()
            logger.info(f"API request successful: {response.status_code}")
            
            data = self._parse_response_data(response)
            return ApiResponse(status_code=response.status_code, data=data)
            
        except requests.HTTPError:
            error_msg = f"HTTP error {response.status_code}: {response.text}"
            logger.error(error_msg)
            return ApiResponse(
                status_code=response.status_code, 
                data=[], 
                message=error_msg
            )
        except requests.RequestException as e:
            error_msg = f"Request failed: {e}"
            logger.error(error_msg)
            raise ApiError(error_msg)

    def _parse_response_data(self, response: requests.Response) -> List[Dict[str, Any]]:
        """Parse response data from JSON."""
        try:
            data = response.json()
            return data if isinstance(data, list) else [data]
        except ValueError:
            logger.warning("Response is not valid JSON")
            return []


def main() -> None:
    """Example usage of the API client."""
    base_url = "https://tkmservices.ibb.gov.tr/web/api/TrafficData/v1"
    
    try:
        client = ApiClient(base_url=base_url)
        response = client.get("/TrafficIndex_Sc1_Cont")

        print("Response from API:")
        print(f"Status code: {response.status_code}")
        print(f"Successful: {response.is_successful}")
        print(f"Has data: {response.has_data}")
        print(f"Data count: {len(response.data)}")
        print(f"Message: {response.message or 'None'}")
        
        if response.has_data:
            print(f"First item: {response.data[0] if response.data else 'None'}")
            
    except ApiError as e:
        logger.error(f"API error: {e}")
        print(f"API error: {e}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
