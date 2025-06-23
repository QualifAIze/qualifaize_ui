from typing import Optional
from ..base_client import BaseApiClient, ApiResponse


class InterviewService(BaseApiClient):
    def __init__(self, auth_token: Optional[str] = None, **kwargs):
        super().__init__(auth_token=auth_token, **kwargs)
        self.base_endpoint = "interview"

    def create_interview(
            self,
            name: str,
            document_id: str,
            description: Optional[str] = None,
            difficulty: str = "MEDIUM",
            assigned_to_user_id: Optional[str] = None,
            scheduled_date: Optional[str] = None
    ) -> ApiResponse:
        interview_data = {
            "name": name,
            "documentId": document_id,
            "difficulty": difficulty
        }

        if description:
            interview_data["description"] = description
        if assigned_to_user_id:
            interview_data["assignedToUserId"] = assigned_to_user_id
        if scheduled_date:
            interview_data["scheduledDate"] = scheduled_date

        return self.post(self.base_endpoint, data=interview_data)

    def change_interview_status(self, interview_id: str, new_status: str) -> ApiResponse:
        params = {"newStatus": new_status}
        return self.get(f"{self.base_endpoint}/{interview_id}", params=params)

    def get_next_question(self, interview_id: str) -> ApiResponse:
        return self.get(f"{self.base_endpoint}/next/{interview_id}")

    def get_assigned_interviews(self, status: Optional[str] = None) -> ApiResponse:
        if status:
            params = {"status": status}
            return self.get(f"{self.base_endpoint}/assigned", params=params)
        else:
            return self.get(f"{self.base_endpoint}/assigned")

    def submit_answer(self, question_id: str, answer: str) -> ApiResponse:
        params = {"correctAnswer": answer.upper()}
        return self.get(f"{self.base_endpoint}/answer/{question_id}", params=params)