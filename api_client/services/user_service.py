from typing import Optional, List
from ..base_client import BaseApiClient, ApiResponse


class UserService(BaseApiClient):
    def __init__(self, auth_token: Optional[str] = None, **kwargs):
        super().__init__(auth_token=auth_token, **kwargs)
        self.base_endpoint = "user"

    def get_all_users(self) -> ApiResponse:
        return self.get(f"{self.base_endpoint}")

    def get_current_user_details(self) -> ApiResponse:
        return self.get(f"{self.base_endpoint}/me")

    def update_user_details(
            self,
            user_id: str,
            username: Optional[str] = None,
            email: Optional[str] = None,
            first_name: Optional[str] = None,
            last_name: Optional[str] = None,
            birth_date: Optional[str] = None
    ) -> ApiResponse:
        update_data = {}

        if username is not None:
            update_data["username"] = username
        if email is not None:
            update_data["email"] = email
        if first_name is not None:
            update_data["firstName"] = first_name
        if last_name is not None:
            update_data["lastName"] = last_name
        if birth_date is not None:
            update_data["birthDate"] = birth_date

        return self.put(f"{self.base_endpoint}/{user_id}", data=update_data)

    def promote_user(self, user_id: str, role: str) -> ApiResponse:
        params = {"role": role}
        return self.get(f"{self.base_endpoint}/promote/{user_id}", params=params)

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
        if roles is None:
            roles = ["GUEST"]

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