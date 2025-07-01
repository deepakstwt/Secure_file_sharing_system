# Secure File Sharing System

## Overview
A production-ready secure file sharing system built with FastAPI and MongoDB, featuring role-based access control, encrypted download links, and a modern web interface.

## Features

### User Management
- **Client User Signup** with email verification
- **Role-based Authentication** (Client/Ops users)
- **JWT Token Security** with expiration

### File Operations
- **File Upload** (Ops users only) - .pptx, .docx, .xlsx
- **Secure Download Links** (Client users only)
- **File Listing** (Client users only)
- **File Type Validation**

### Security Features
- **Encrypted Download URLs** with JWT tokens
- **Role-based Access Control**
- **Password Hashing** (bcrypt)
- **Token Expiration** (10 minutes for download links)

### Web Interface
- **Modern responsive UI** (HTML/CSS/JS, glassmorphism design)
- **Login/Signup forms** for both user types
- **Drag & drop file upload** (Ops)
- **Interactive file browser** (Client)
- **Real-time notifications**
- **Mobile-friendly**

## API Endpoints

### Authentication
- `POST /auth/client/signup` - Client user registration
- `GET /auth/verify-email/{token}` - Email verification
- `POST /auth/client/login` - Client user login
- `POST /auth/ops/login` - Operations user login
- `POST /auth/token` - OAuth2 token endpoint

### File Management
- `POST /file/upload` - Upload files (Ops only)
- `GET /file/list` - List all files (Client only)
- `GET /file/download/{file_id}` - Generate download link (Client only)
- `GET /file/actual-download/{token}` - Secure file download

### System
- `/` - Home
- `/health` - Health check
- `/web` - Web UI

## Tech Stack
- **Backend**: FastAPI (Python 3.9+)
- **Database**: MongoDB Atlas
- **Authentication**: JWT tokens
- **Password Hashing**: bcrypt
- **Frontend**: HTML, CSS (glassmorphism), JavaScript
- **File Storage**: Local filesystem

## Installation & Setup

1. **Clone the repository**
```bash
git clone <repository-url>
cd secure-file-sharing
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
# Create .env file in secure-file-sharing/
MONGO_URL=mongodb+srv://<username>:<password>@cluster.mongodb.net/secure_file_sharing
SECRET_KEY=your-secret-key-here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=120
DOWNLOAD_TOKEN_EXPIRE_MINUTES=10
```

5. **Run the application**
```bash
uvicorn app.main:app --reload --port 8009
```

6. **Access the App**
- **Web Interface**: http://127.0.0.1:8009/web
- **API Documentation**: http://127.0.0.1:8009/docs
- **Health Check**: http://127.0.0.1:8009/health

## Web Interface Usage
- Go to http://127.0.0.1:8009/web
- Use the navigation bar to Login or Sign Up
- Ops users can upload files (.pptx, .docx, .xlsx)
- Client users can list and download files
- All actions are protected by role-based authentication

## API Testing

### Swagger UI
- Visit http://127.0.0.1:8009/docs for interactive API docs

### Postman
- Use the provided `Secure_File_Sharing_API.postman_collection.json` and `Secure_File_Sharing.postman_environment.json` for quick API testing

## Project Structure
```
secure-file-sharing/
├── app/
│   ├── db/
│   │   └── mongo.py          # Database connection
│   ├── models/               # Data models
│   ├── routes/               # API routes
│   ├── schemas/              # Pydantic schemas
│   ├── utils/                # Utility functions
│   └── main.py               # FastAPI application
├── static/
│   ├── css/style.css         # Web UI styles
│   └── js/app.js             # Web UI scripts
├── templates/
│   └── index.html            # Web UI template
├── uploads/                  # File storage directory
├── test_cases.py             # Test cases
├── requirements.txt          # Dependencies
├── DEPLOYMENT.md             # Production deployment guide
├── WEB_UI_GUIDE.md           # Web UI usage guide
├── Secure_File_Sharing_API.postman_collection.json
├── Secure_File_Sharing.postman_environment.json
└── README.md                 # This file
```

## Security Considerations

### Production Deployment
- Use a strong SECRET_KEY
- Enable HTTPS/TLS
- Set up rate limiting
- Configure CORS properly
- Use cloud storage (AWS S3/Google Cloud) for files in production
- Implement proper logging and monitoring

### Current Security Features
- Password hashing with bcrypt
- JWT token authentication
- Role-based access control
- File type validation
- Secure download links with expiration

## Testing

### Run Test Suite
```bash
python test_cases.py
```

### Manual Testing
- Use the web interface for end-to-end flows
- Use Swagger UI or Postman for API endpoint testing

## Requirements Compliance

- **Framework**: FastAPI (Python)
- **Database**: MongoDB (NoSQL)
- **Ops User**: Login + File Upload (.pptx, .docx, .xlsx only)
- **Client User**: Signup + Email Verify + Login + Download + List Files
- **Secure Download**: Encrypted URLs with JWT tokens
- **Role-based Access**: Proper authorization controls
- **Test Cases**: Comprehensive test suite
- **Production Plan**: Deployment documentation
- **Web UI**: Modern, responsive, glassmorphism design

## License
This project is licensed under the MIT License.

## Support
For issues and questions, please create an issue in the repository. 