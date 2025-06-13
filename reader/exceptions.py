"""Custom exceptions for the IBB Traffic Data API reader."""

from typing import Optional


class ApiError(Exception):
    """Custom exception for API-related errors."""
    
    def __init__(self, message: str, status_code: Optional[int] = None):
        super().__init__(message)
        self.status_code = status_code


class ApiConnectionError(ApiError):
    """Exception raised when API connection fails."""
    pass


class ApiTimeoutError(ApiError):
    """Exception raised when API request times out."""
    pass


class ApiHttpError(ApiError):
    """Exception raised for HTTP-related API errors."""
    pass


class ApiParsingError(ApiError):
    """Exception raised when API response cannot be parsed."""
    pass
