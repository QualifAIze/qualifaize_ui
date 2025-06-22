from typing import Optional, List
from ..base_client import BaseApiClient, ApiResponse


class UserService(BaseApiClient):
    def __init__(self, auth_token: Optional[str] = None, **kwargs):
        super().__init__(auth_token=auth_token, **kwargs)
        self.base_endpoint = "user"

    def get_all_users(self) -> ApiResponse:
        return self.get(f"{self.base_endpoint}")

    def login(self, username: str, password: str) -> ApiResponse:
        login_data = {
            "username": username,
            "password": password
        }
        return self.post(f"{self.base_endpoint}/auth/login", data=login_data)

    def register(
            self,
            username: str,
            password: str,
            email: str,
            first_name: str,
            last_name: str,
            birth_date: str,
            roles: Optional[List[str]] = None
    ) -> ApiResponse:

        registration_data = {
            "username": username,
            "password": password,
            "email": email,
            "firstName": first_name,
            "lastName": last_name,
            "birthDate": birth_date,
            "roles": roles
        }
        return self.post(f"{self.base_endpoint}/auth/register", data=registration_data)

    def delete_user(self, user_id: str) -> ApiResponse:
        return self.delete(f"{self.base_endpoint}/{user_id}")
