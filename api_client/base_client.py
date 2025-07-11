import json
import logging
from dataclasses import dataclass
from typing import Dict, Any, Optional
from urllib.parse import urljoin
import streamlit as st

import requests

from constants import BACKEND_BASE_URL, BACKEND_BASE_PATH, DEFAULT_TIMEOUT, BEARER_PREFIX, HTTP_SUCCESS_MIN, \
    HTTP_SUCCESS_MAX


@dataclass
class ApiResponse:
    success: bool
    status_code: int
    data: Optional[Any] = None
    error: Optional[str] = None
    headers: Optional[Dict[str, str]] = None

    @property
    def is_success(self) -> bool:
        return self.success and HTTP_SUCCESS_MIN <= self.status_code < HTTP_SUCCESS_MAX


class ApiException(Exception):
    def __init__(self, message: str, status_code: int = None, response_data: Any = None):
        super().__init__(message)
        self.status_code = status_code
        self.response_data = response_data


class BaseApiClient:
    def __init__(self, auth_token: Optional[str] = None, timeout: int = DEFAULT_TIMEOUT,
                 base_url: str = BACKEND_BASE_URL, base_path: str = BACKEND_BASE_PATH):
        self.base_url = base_url.rstrip('/')
        self.base_path = base_path.strip('/')
        self.timeout = timeout
        self.session = requests.Session()
        self.logger = logging.getLogger(self.__class__.__name__)

        # Set default headers for JSON requests only
        self.session.headers.update({
            'Accept': 'application/json'
        })

        if auth_token:
            self.set_auth_token(auth_token)

    def set_auth_token(self, token: str) -> None:
        self.session.headers.update({
            'Authorization': f'{BEARER_PREFIX} {token}'
        })

    def clear_auth_token(self) -> None:
        self.session.headers.pop('Authorization', None)

    def _build_url(self, endpoint: str) -> str:
        if endpoint.startswith('/'):
            endpoint = endpoint[1:]
        if self.base_path:
            full_path = f"{self.base_path}/{endpoint}"
        else:
            full_path = endpoint
        return urljoin(f"{self.base_url}/", full_path)

    def _handle_response(self, response: requests.Response) -> ApiResponse:
        try:
            data = response.json() if response.content else None
        except json.JSONDecodeError:
            data = response.text if response.content else None

        success = HTTP_SUCCESS_MIN <= response.status_code < HTTP_SUCCESS_MAX

        error = None
        if not success:
            if isinstance(data, dict):
                error = data.get('message', data.get('error', f'HTTP {response.status_code}'))
            else:
                error = f'HTTP {response.status_code}: {response.reason}'

        return ApiResponse(
            success=success,
            status_code=response.status_code,
            data=data,
            error=error,
            headers=dict(response.headers)
        )

    def _make_request(
            self,
            method: str,
            endpoint: str,
            data: Optional[Dict[str, Any]] = None,
            params: Optional[Dict[str, Any]] = None,
            files: Optional[Dict[str, Any]] = None,
            headers: Optional[Dict[str, str]] = None
    ) -> ApiResponse:
        url = self._build_url(endpoint)

        # Start with clean headers for this request
        request_headers = {}

        # Get auth headers from session state
        if st.session_state.authenticated_user is not None:
            logged_user = st.session_state.authenticated_user
            auth_token = logged_user.get("token")
            if auth_token:
                request_headers["Authorization"] = f"Bearer {auth_token}"

        # Add any additional headers passed to the method
        if headers:
            request_headers.update(headers)

        kwargs = {
            'timeout': self.timeout,
            'params': params,
        }

        if files:
            # For multipart/form-data requests (file uploads)
            kwargs['files'] = files
            if data:
                # Add form data alongside files
                kwargs['data'] = data

            # CRITICAL: Only add Accept header for file uploads, let requests handle Content-Type
            request_headers = {k: v for k, v in request_headers.items() if k != 'Content-Type'}
            request_headers['Accept'] = 'application/json'
            kwargs['headers'] = request_headers

        else:
            # For regular JSON requests
            request_headers['Content-Type'] = 'application/json'
            request_headers['Accept'] = 'application/json'
            kwargs['headers'] = request_headers

            if data is not None:
                kwargs['json'] = data

        try:
            self.logger.debug(f"Making {method} request to {url}")
            self.logger.debug(f"Headers: {kwargs.get('headers', {})}")
            if files:
                self.logger.debug(f"Files: {list(files.keys()) if files else None}")
                self.logger.debug(f"Form data: {data}")

            response = self.session.request(method, url, **kwargs)

            api_response = self._handle_response(response)

            if not api_response.is_success:
                self.logger.warning(f"API request failed: {api_response.error}")

            return api_response

        except requests.exceptions.Timeout:
            raise ApiException(f"Request timeout after {self.timeout} seconds")
        except requests.exceptions.ConnectionError:
            raise ApiException(f"Connection error to {url}")
        except requests.exceptions.RequestException as e:
            raise ApiException(f"Request failed: {str(e)}")

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None, **kwargs) -> ApiResponse:
        return self._make_request('GET', endpoint, params=params, **kwargs)

    def post(self, endpoint: str, data: Optional[Dict[str, Any]] = None, **kwargs) -> ApiResponse:
        return self._make_request('POST', endpoint, data=data, **kwargs)

    def put(self, endpoint: str, data: Optional[Dict[str, Any]] = None, **kwargs) -> ApiResponse:
        return self._make_request('PUT', endpoint, data=data, **kwargs)

    def patch(self, endpoint: str, data: Optional[Dict[str, Any]] = None, **kwargs) -> ApiResponse:
        return self._make_request('PATCH', endpoint, data=data, **kwargs)

    def delete(self, endpoint: str, **kwargs) -> ApiResponse:
        return self._make_request('DELETE', endpoint, **kwargs)