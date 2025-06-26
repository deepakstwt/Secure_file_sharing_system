#!/usr/bin/env python3

import requests
import json
import os
from datetime import datetime

BASE_URL = "http://127.0.0.1:8009"
CLIENT_EMAIL = "client@company.com"
CLIENT_PASSWORD = "Pro12345"

def print_header():
    print("=" * 60)
    print("🔒 SECURE FILE SHARING - DOCUMENT DOWNLOADER")
    print("=" * 60)

def login_client():
    print("📋 Step 1: Logging in as client user...")
    
    try:
        response = requests.post(f"{BASE_URL}/auth/client/login", json={
            "email": CLIENT_EMAIL,
            "password": CLIENT_PASSWORD
        })
        
        if response.status_code == 200:
            token = response.json()["access_token"]
            print("✅ Login successful!")
            return token
        else:
            print(f"❌ Login failed: {response.json().get('detail', 'Unknown error')}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection error: {e}")
        print("💡 Make sure the server is running on http://127.0.0.1:8009")
        return None

def list_files(token):
    print("\n📂 Step 2: Fetching available files...")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(f"{BASE_URL}/file/list", headers=headers)
        
        if response.status_code == 200:
            files_data = response.json()
            files = files_data["files"]
            
            if not files:
                print("📭 No files available for download")
                return []
            
            print(f"✅ Found {len(files)} file(s):")
            print("-" * 50)
            
            for i, file_info in enumerate(files, 1):
                print(f"{i}. {file_info['filename']}")
                print(f"   📄 Type: {file_info['file_type']}")
                print(f"   👤 Uploaded by: {file_info['uploader']}")
                print(f"   🆔 ID: {file_info['file_id']}")
                print()
            
            return files
        else:
            print(f"❌ Failed to fetch files: {response.json().get('detail', 'Unknown error')}")
            return []
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection error: {e}")
        return []

def generate_download_link(token, file_id, filename):
    print(f"🔗 Step 3: Generating secure download link for '{filename}'...")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(f"{BASE_URL}/file/download/{file_id}", headers=headers)
        
        if response.status_code == 200:
            download_link = response.json()["download_link"]
            print("✅ Secure download link generated!")
            print("⏰ Link expires in 10 minutes")
            return download_link
        else:
            print(f"❌ Failed to generate link: {response.json().get('detail', 'Unknown error')}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection error: {e}")
        return None

def download_file(download_link, filename):
    print(f"\n💾 Step 4: Downloading '{filename}'...")
    
    try:
        response = requests.get(download_link)
        
        if response.status_code == 200:
            # Create downloads directory if it doesn't exist
            os.makedirs("downloads", exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_filename = f"downloads/{timestamp}_{filename}"
            
            with open(safe_filename, "wb") as f:
                f.write(response.content)
            
            file_size = len(response.content)
            print(f"✅ File downloaded successfully!")
            print(f"📁 Saved as: {safe_filename}")
            print(f"📏 Size: {file_size} bytes")
            
            return safe_filename
        else:
            print(f"❌ Download failed: Status {response.status_code}")
            if response.status_code == 401:
                print("🔒 Download link may have expired (10-minute limit)")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Download error: {e}")
        return None

def main():
    print_header()
    
    token = login_client()
    if not token:
        return
    
    files = list_files(token)
    if not files:
        return
    
    print("🎯 Select a file to download:")
    try:
        while True:
            choice = input(f"Enter number (1-{len(files)}) or 'q' to quit: ").strip()
            
            if choice.lower() == 'q':
                print("👋 Goodbye!")
                return
            
            try:
                file_index = int(choice) - 1
                if 0 <= file_index < len(files):
                    selected_file = files[file_index]
                    break
                else:
                    print(f"❌ Please enter a number between 1 and {len(files)}")
            except ValueError:
                print("❌ Please enter a valid number or 'q' to quit")
    
    except KeyboardInterrupt:
        print("\n\n👋 Download cancelled by user")
        return
    
    download_link = generate_download_link(
        token, 
        selected_file["file_id"], 
        selected_file["filename"]
    )
    
    if not download_link:
        return
    
    downloaded_file = download_file(download_link, selected_file["filename"])
    
    if downloaded_file:
        print("\n" + "=" * 60)
        print("🎉 DOWNLOAD COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        print(f"📂 File location: {os.path.abspath(downloaded_file)}")
        print("\n🔒 Security Features Used:")
        print("   ✓ JWT Authentication")
        print("   ✓ Role-based Access Control")
        print("   ✓ Encrypted Download Links")
        print("   ✓ 10-minute Link Expiry")

if __name__ == "__main__":
    main() 