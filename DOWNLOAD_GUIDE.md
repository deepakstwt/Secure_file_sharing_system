# Document Download Guide

## Overview
This guide explains how to download documents from the Secure File Sharing System using different methods.

## Prerequisites
- Server running on http://127.0.0.1:8009
- Client user account (email ending with any domain)
- Available files uploaded by Ops users

## Method 1: Using Swagger UI (Easiest)

### Step 1: Open Swagger UI
1. Go to: http://127.0.0.1:8009/docs
2. You'll see the interactive API documentation

### Step 2: Authenticate
1. Click on **"Authorize"** button (lock icon)
2. Use OAuth2 form:
   - **Username**: client@company.com
   - **Password**: Pro12345
3. Click **"Authorize"** and then **"Close"**

### Step 3: List Available Files
1. Find **"File Management"** section
2. Click on **GET /file/list**
3. Click **"Try it out"**
4. Click **"Execute"**
5. Copy a **file_id** from the response

### Step 4: Generate Download Link
1. Click on **GET /file/download/{file_id}**
2. Click **"Try it out"**
3. Paste the **file_id** in the parameter field
4. Click **"Execute"**
5. Copy the **download_link** from response

### Step 5: Download File
1. Open the **download_link** in a new browser tab
2. File will download automatically

## Method 2: Using cURL Commands

### Step 1: Login and Get Token
```bash
curl -X POST "http://127.0.0.1:8009/auth/client/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "client@company.com", "password": "Pro12345"}'
```

Save the `access_token` from response.

### Step 2: List Files
```bash
curl -X GET "http://127.0.0.1:8009/file/list" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Step 3: Generate Download Link
```bash
curl -X GET "http://127.0.0.1:8009/file/download/FILE_ID" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Step 4: Download File
```bash
curl -X GET "DOWNLOAD_LINK_FROM_STEP_3" \
  -o "my_document.xlsx"
```

## Method 3: Using Python Script

```python
import requests
import json

# Configuration
BASE_URL = "http://127.0.0.1:8009"
CLIENT_EMAIL = "client@company.com"
CLIENT_PASSWORD = "Pro12345"

def download_document():
    # Step 1: Login
    login_response = requests.post(f"{BASE_URL}/auth/client/login", json={
        "email": CLIENT_EMAIL,
        "password": CLIENT_PASSWORD
    })
    
    if login_response.status_code != 200:
        print("Login failed!")
        return
    
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # Step 2: List files
    files_response = requests.get(f"{BASE_URL}/file/list", headers=headers)
    files_data = files_response.json()
    
    print("Available files:")
    for file_info in files_data["files"]:
        print(f"- {file_info['filename']} (ID: {file_info['file_id']})")
    
    # Step 3: Select first file and generate download link
    if files_data["files"]:
        file_id = files_data["files"][0]["file_id"]
        filename = files_data["files"][0]["filename"]
        
        download_response = requests.get(
            f"{BASE_URL}/file/download/{file_id}", 
            headers=headers
        )
        
        download_link = download_response.json()["download_link"]
        
        # Step 4: Download the file
        file_response = requests.get(download_link)
        
        if file_response.status_code == 200:
            with open(f"downloaded_{filename}", "wb") as f:
                f.write(file_response.content)
            print(f"File downloaded as: downloaded_{filename}")
        else:
            print("Download failed!")

if __name__ == "__main__":
    download_document()
```

## Security Features

### Download Link Security
- **JWT Encryption**: Download links are encrypted using JWT tokens
- **Time Expiry**: Links expire after 10 minutes for security
- **Role Verification**: Only client users can generate download links
- **Single Use**: Each link is unique and secure

### Access Control
- **Authentication Required**: Must login as client user
- **Role-based Access**: Only clients can download, only ops can upload
- **File Type Validation**: Only .pptx, .docx, .xlsx files allowed

## Troubleshooting

### Common Issues

1. **"Unauthorized" Error**
   - Check if you're logged in as a client user
   - Verify your access token is valid

2. **"Download link expired"**
   - Generate a new download link (10-minute expiry)
   - Use the link immediately after generation

3. **"File not found"**
   - Verify the file_id is correct
   - Check if file exists in the system

4. **Server Connection Error**
   - Ensure server is running on port 8009
   - Check if virtual environment is activated

### Server Status Check
```bash
curl -X GET "http://127.0.0.1:8009/health"
```
Should return: `{"status": "healthy"}`

## Example Response Flow

### 1. Login Response
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 2. File List Response
```json
{
  "files": [
    {
      "file_id": "685ae3d2adc1a66a8ffd9ca6",
      "filename": "document.xlsx",
      "file_type": "xlsx",
      "uploader": "ops",
      "uploaded_at": "2024-01-20T10:30:00"
    }
  ],
  "total_files": 1
}
```

### 3. Download Link Response
```json
{
  "download_link": "http://127.0.0.1:8009/file/actual-download/eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmaWxlX2lkIjoiNjg1YWUzZDJhZGMxYTY2YThmZmQ5Y2E2Iiwicm9sZSI6ImNsaWVudCIsImV4cCI6MTc1MDc4OTQwNX0.qLpHAlmZ4hZc_S_9UzOqmkU4qO_g8U3f-YZh6iqyLcA",
  "message": "success"
}
```

## Quick Start

For immediate testing:

1. **Start Server**: `uvicorn app.main:app --reload --port 8009`
2. **Open Browser**: Go to http://127.0.0.1:8009/docs
3. **Login**: Use client@company.com / Pro12345
4. **List Files**: Execute GET /file/list
5. **Download**: Use file_id to generate download link

That's it! Your file will be downloaded securely with full encryption and role-based access control. 