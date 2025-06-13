"""Istanbul Municipality Traffic Data Reader.

This module provides a simple API client for accessing IBB traffic data.
"""

from .api import ApiClient, ApiResponse


__version__ = "0.1.0"
__author__ = "utkuyucel"
__all__ = ["ApiClient", "ApiResponse"]
