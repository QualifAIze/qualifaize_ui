# QualifAIze UI

AI-powered interview platform frontend built with Streamlit for automated technical interview generation and management.

## Overview

QualifAIze UI provides an intelligent interview system that automatically generates technical questions based on uploaded documents using AI, with real-time question generation and adaptive difficulty adjustment.

## Features

- **AI-Driven Interviews**: Dynamic question generation using GPT-4 models
- **Document-Based Questions**: Upload PDFs to generate relevant technical questions
- **User Management**: Role-based access control (Guest, User, Admin)
- **Interview Analytics**: Performance tracking and detailed feedback
- **Secure Authentication**: JWT-based authentication with Spring Boot backend integration

## Quick Start

### Prerequisites
- Python 3.10+
- QualifAIze Backend API running on port 8080

### Installation
```bash
# Clone repository
git clone https://github.com/QualifAIze/qualifaize_ui.git
cd qualifaize_ui

# Create environment
conda create -n qualifaize python=3.10
conda activate qualifaize

# Install dependencies
pip install -r requirements.txt

# Run application
streamlit run ui.py
```

Application available at `http://localhost:8501`

## Architecture

### Tech Stack
- **Frontend**: Streamlit, Python
- **API Client**: Requests with JWT authentication
- **Backend Integration**: RESTful API communication with Spring Boot
- **Authentication**: JWT tokens with HS512 algorithm

### Project Structure
```
qualifaize_ui/
├── api_client/           # API communication layer
├── pages/               # Streamlit page components
├── dialogs/             # Modal dialog components
├── custom_styles.py     # CSS styling
├── constants.py         # App constants
└── ui.py               # Main navigation
```

## Configuration

### Backend Connection
```python
BACKEND_BASE_URL = "http://localhost:8080"
BACKEND_BASE_PATH = "api/v1"
```

### User Roles
- **GUEST**: Take assigned interviews
- **USER**: Interview participation + history access
- **ADMIN**: Full system access including user/document management

## Development

### API Integration Pattern
```python
class NewService(BaseApiClient):
    def __init__(self, auth_token: Optional[str] = None, **kwargs):
        super().__init__(auth_token=auth_token, **kwargs)
        self.base_endpoint = "new-endpoint"
    
    def create_resource(self, data: dict) -> ApiResponse:
        return self.post(self.base_endpoint, data=data)
```

### Key Backend Endpoints
- `POST /api/v1/user/auth/login` - Authentication
- `GET /api/v1/interview/assigned` - Get assigned interviews
- `POST /api/v1/pdf` - Document upload
- `GET /api/v1/interview/next/{id}` - Get next question

## Dependencies

```
streamlit~=1.46.0          # Web framework
requests~=2.32.4           # HTTP client
python-jose[cryptography]   # JWT handling
```

## Troubleshooting

**Backend Connection Issues**
```bash
curl http://localhost:8080/api/v1/health
netstat -tlnp | grep 8080
```

**Common Problems**
- Ensure JWT secret matches backend configuration
- Check token expiration (24-hour default)
- Maximum file size: 50MB, PDF only

## License

MIT License - see LICENSE file for details.

---

**Note**: Requires QualifAIze Backend API to be running and properly configured.