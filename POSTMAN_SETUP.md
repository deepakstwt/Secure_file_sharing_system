# Postman Collection Setup Guide

## Files Included

1. **`Secure_File_Sharing_API.postman_collection.json`** - Complete API collection
2. **`Secure_File_Sharing.postman_environment.json`** - Environment variables
3. **`POSTMAN_SETUP.md`** - This setup guide

## Quick Setup

### Step 1: Import Collection
1. Open Postman
2. Click **Import** button (top left)
3. Drag & drop `Secure_File_Sharing_API.postman_collection.json`
4. Click **Import**

### Step 2: Import Environment
1. Click **Import** again
2. Drag & drop `Secure_File_Sharing.postman_environment.json`
3. Click **Import**

### Step 3: Select Environment
1. Click the environment dropdown (top right)
2. Select **"Secure File Sharing Environment"**

### Step 4: Start Your Server
Make sure your FastAPI server is running:
```bash
cd secure-file-sharing
python -m uvicorn app.main:app --host 0.0.0.0 --port 8009 --reload
```

## Testing Workflow

### 1. System Health Check
- Run: **System → Health Check**
- Should return: `{"status": "healthy"}`

### 2. User Registration
- Run: **Authentication → Client Signup**
- Creates a new client user
- Check email for verification (if configured)

### 3. Email Verification (Optional)
- Update `{{verification_token}}` variable with token from email
- Run: **Authentication → Verify Email**

### 4. Login as Client User
- Run: **Authentication → Client Login**
- **Auto-saves token** to `CLIENT_TOKEN` variable

### 5. Login as Ops User
- Update credentials in **Authentication → Ops Login**
- Run the request
- **Auto-saves token** to `OPS_TOKEN` variable

### 6. Upload File (Ops User)
- Run: **File Operations → Upload File (Ops Only)**
- Select a `.xlsx`, `.docx`, or `.pptx` file
- Returns file metadata with `file_id`

### 7. List Files (Client User)
- Run: **File Operations → List Files (Client Only)**
- Shows all uploaded files
- Copy a `file_id` for download testing

### 8. Generate Download Link
- Update `{{file_id}}` variable with actual file ID
- Run: **File Operations → Generate Download Link (Client Only)**
- **Auto-saves** secure URL to `DOWNLOAD_URL` variable

### 9. Download File
- Run: **File Operations → Secure File Download**
- Uses the auto-saved download URL
- Downloads the actual file

## Environment Variables

| Variable | Description | Auto-populated |
|----------|-------------|----------------|
| `BASE_URL` | API base URL | Manual |
| `CLIENT_TOKEN` | Client JWT token | Auto (after login) |
| `OPS_TOKEN` | Ops JWT token | Auto (after login) |
| `TOKEN_TYPE` | Bearer token type | Pre-set |
| `DOWNLOAD_URL` | Secure download link | Auto (after requesting) |
| `file_id` | File ID for operations | Manual (copy from responses) |
| `verification_token` | Email verification token | Manual (from email) |

## API Endpoints Overview

### Authentication (5 endpoints)
- `POST /auth/client/signup` - User registration
- `GET /auth/verify-email/{token}` - Email verification
- `POST /auth/client/login` - Client login
- `POST /auth/ops/login` - Ops login
- `POST /auth/token` - OAuth2 token

### File Operations (4 endpoints)
- `POST /file/upload` - Upload file (Ops only)
- `GET /file/list` - List files (Client only)
- `GET /file/download/{file_id}` - Generate download link (Client only)
- `GET /file/actual-download/{token}` - Secure download

### System (1 endpoint)
- `GET /health` - Health check

## Security Features

### Role-Based Access
- **Ops Users**: Can only upload files
- **Client Users**: Can only list and download files
- Cross-role access attempts return `403 Forbidden`

### Secure Downloads
- Download links expire in **10 minutes**
- URLs are JWT-encrypted
- No authentication required for actual download (URL contains embedded auth)

### File Restrictions
- Only `.pptx`, `.docx`, `.xlsx` files allowed
- Other file types rejected with error

## Test Scripts Included

The collection includes automated test scripts that:
- Auto-save JWT tokens after successful login
- Auto-save download URLs after generation
- Validate response status codes
- Set environment variables for chaining requests

## Pro Tips

1. **Use Runner**: Select the collection and run all requests in sequence
2. **Environment Switching**: Create separate environments for dev/staging/prod
3. **Variable Copying**: Right-click variables to copy values
4. **Request Chaining**: Use test scripts to pass data between requests
5. **File Upload**: Use the file selector in form-data body for uploads

## Troubleshooting

### Common Issues

1. **401 Unauthorized**
   - Make sure you're logged in
   - Check if token is saved in environment variables
   - Verify token hasn't expired (2 hours for login)

2. **403 Forbidden**
   - Check user role permissions
   - Ops users can't download, Client users can't upload

3. **422 Validation Error**
   - Check request body format
   - Ensure required fields are present
   - Verify file type for uploads

4. **Connection Error**
   - Ensure server is running on port 8009
   - Check `BASE_URL` environment variable

### Server Logs
Check server logs for detailed error information:
```bash
tail -f server.log
```

## Additional Resources

- **Swagger UI**: `http://localhost:8009/docs`
- **ReDoc**: `http://localhost:8009/redoc`
- **GitHub Repository**: https://github.com/deepakstwt/Secure_file_sharing_system
- **Download Guide**: See `DOWNLOAD_GUIDE.md`
- **Deployment Guide**: See `DEPLOYMENT.md`

---

**Happy Testing!** 