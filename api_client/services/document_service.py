from typing import Optional, BinaryIO
from ..base_client import BaseApiClient, ApiResponse


class DocumentService(BaseApiClient):
    def __init__(self, auth_token: Optional[str] = None, **kwargs):
        super().__init__(auth_token=auth_token, **kwargs)
        self.base_endpoint = "pdf"

    def upload_pdf(self, file_path: str, secondary_file_name: str) -> ApiResponse:
        try:
            with open(file_path, 'rb') as file:
                return self.upload_pdf_from_buffer(file, secondary_file_name, file_path)
        except FileNotFoundError:
            from ..base_client import ApiException
            raise ApiException(f"File not found: {file_path}")

    def upload_pdf_from_buffer(
            self,
            file_buffer: BinaryIO,
            secondary_file_name: str,
            filename: str = "document.pdf"
    ) -> ApiResponse:
        files = {
            'file': (filename, file_buffer, 'application/pdf')
        }
        data = {
            'secondary_file_name': secondary_file_name
        }
        return self._make_request('POST', self.base_endpoint, data=data, files=files)

    def get_all_documents(self) -> ApiResponse:
        return self.get(self.base_endpoint)

    def get_document_with_toc(self, document_id: str) -> ApiResponse:
        return self.get(f"{self.base_endpoint}/{document_id}")

    def get_document_content(self, document_id: str, subsection_name: str) -> ApiResponse:
        return self.get(f"{self.base_endpoint}/{document_id}/{subsection_name}")

    def update_document_title(self, document_id: str, new_title: str) -> ApiResponse:
        params = {"title": new_title}
        return self.patch(f"{self.base_endpoint}/{document_id}", params=params)

    def delete_document(self, document_id: str) -> ApiResponse:
        return self.delete(f"{self.base_endpoint}/{document_id}")