import streamlit as st
from api_client.services.user_service import UserService
from base_client import ApiException
import logging

logger = logging.getLogger(__name__)


class AuthHandler:
    def __init__(self):
        self.user_service = UserService()

    def login(self, username: str, password: str) -> bool:
        try:
            response = self.user_service.login(username, password)

            if response.is_success:
                token = response.data.get("token")

                user_object = {
                    "token": token,
                    "username": username,
                    "auth_headers": {
                        "Authorization": f"Bearer {token}",
                        "Content-Type": "application/json"
                    },
                    "login_time": st.session_state.get("current_time", None)
                }

                st.session_state["authenticatedUser"] = user_object

                logger.info(f"User {username} logged in successfully")
                return True
            else:
                logger.warning(f"Login failed for user {username}: {response.error}")
                return False

        except ApiException as e:
            logger.error(f"API error during login: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error during login: {e}")
            return False

    def logout(self):
        """Clear authentication session state"""
        if "authenticatedUser" in st.session_state:
            del st.session_state["authenticatedUser"]
        logger.info("User logged out")

    def is_authenticated(self) -> bool:
        """Check if user is currently authenticated"""
        return "authenticatedUser" in st.session_state and st.session_state["authenticatedUser"] is not None

    def get_auth_token(self) -> str:
        """Get current auth token"""
        user = st.session_state.get("authenticatedUser")
        return user.get("token", "") if user else ""

    def get_username(self) -> str:
        """Get current username"""
        user = st.session_state.get("authenticatedUser")
        return user.get("username", "") if user else ""

    def get_auth_headers(self) -> dict:
        """Get auth headers for API requests"""
        user = st.session_state.get("authenticatedUser")
        return user.get("auth_headers", {}) if user else {}

    def get_user_object(self) -> dict:
        """Get complete user object"""
        return st.session_state.get("authenticatedUser", {})
