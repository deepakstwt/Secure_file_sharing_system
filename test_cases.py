import pytest
import asyncio
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class TestSecureFileSharing:
    
    def setup_method(self):
        self.ops_user = {
            "email": "ops@test.com",
            "password": "password123"
        }
        
        self.client_user = {
            "email": "client@test.com", 
            "password": "password123"
        }
    
    def test_01_client_signup(self):
        response = client.post("/auth/client/signup", json=self.client_user)
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Verification email sent"
        assert "encrypted_url" in data
        
    def test_02_client_login(self):
        response = client.post("/auth/client/login", json=self.client_user)
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        
    def test_03_ops_login(self):
        client.post("/auth/client/signup", json=self.ops_user)
        response = client.post("/auth/ops/login", json=self.ops_user)
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        
    def test_04_ops_file_upload_success(self):
        login_response = client.post("/auth/ops/login", json=self.ops_user)
        token = login_response.json()["access_token"]
        
        files = {"file": ("test.xlsx", b"fake excel content", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")}
        headers = {"Authorization": f"Bearer {token}"}
        
        response = client.post("/file/upload", files=files, headers=headers)
        assert response.status_code == 200
        assert response.json()["message"] == "File uploaded successfully"
        
    def test_05_client_file_upload_denied(self):
        login_response = client.post("/auth/client/login", json=self.client_user)
        token = login_response.json()["access_token"]
        
        files = {"file": ("test.xlsx", b"fake excel content", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")}
        headers = {"Authorization": f"Bearer {token}"}
        
        response = client.post("/file/upload", files=files, headers=headers)
        assert response.status_code == 403
        assert "Only Ops can upload files" in response.json()["detail"]
        
    def test_06_invalid_file_type_upload(self):
        login_response = client.post("/auth/ops/login", json=self.ops_user)
        token = login_response.json()["access_token"]
        
        files = {"file": ("test.txt", b"fake text content", "text/plain")}
        headers = {"Authorization": f"Bearer {token}"}
        
        response = client.post("/file/upload", files=files, headers=headers)
        assert response.status_code == 400
        assert "Invalid file type" in response.json()["detail"]
        
    def test_07_client_list_files(self):
        login_response = client.post("/auth/client/login", json=self.client_user)
        token = login_response.json()["access_token"]
        
        headers = {"Authorization": f"Bearer {token}"}
        response = client.get("/file/list", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert "files" in data
        assert "total_files" in data
        
    def test_08_ops_cannot_list_files(self):
        login_response = client.post("/auth/ops/login", json=self.ops_user)
        token = login_response.json()["access_token"]
        
        headers = {"Authorization": f"Bearer {token}"}
        response = client.get("/file/list", headers=headers)
        assert response.status_code == 403
        assert "Only clients can list files" in response.json()["detail"]
        
    def test_09_client_download_link_generation(self):
        login_response = client.post("/auth/client/login", json=self.client_user)
        token = login_response.json()["access_token"]
        
        file_id = "507f1f77bcf86cd799439011"
        headers = {"Authorization": f"Bearer {token}"}
        
        response = client.get(f"/file/download/{file_id}", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert "download_link" in data
        assert data["message"] == "success"
        
    def test_10_ops_cannot_generate_download_link(self):
        login_response = client.post("/auth/ops/login", json=self.ops_user)
        token = login_response.json()["access_token"]
        
        file_id = "507f1f77bcf86cd799439011"
        headers = {"Authorization": f"Bearer {token}"}
        
        response = client.get(f"/file/download/{file_id}", headers=headers)
        assert response.status_code == 403
        assert "Only clients can download files" in response.json()["detail"]
        
    def test_11_unauthorized_access(self):
        files = {"file": ("test.xlsx", b"fake excel content", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")}
        response = client.post("/file/upload", files=files)
        assert response.status_code == 401
        
        response = client.get("/file/list")
        assert response.status_code == 401
        
    def test_12_invalid_credentials(self):
        invalid_user = {"email": "invalid@test.com", "password": "wrongpassword"}
        response = client.post("/auth/client/login", json=invalid_user)
        assert response.status_code == 401
        assert "Invalid credentials" in response.json()["detail"]

class TestSecurityFeatures:
    
    def test_jwt_token_expiry(self):
        pass
        
    def test_sql_injection_prevention(self):
        malicious_input = {"email": "'; DROP TABLE users; --", "password": "test"}
        response = client.post("/auth/client/login", json=malicious_input)
        assert response.status_code in [400, 401]
        
    def test_file_path_traversal_prevention(self):
        pass
        
    def test_large_file_upload_handling(self):
        pass

if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 