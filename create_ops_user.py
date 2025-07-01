#!/usr/bin/env python3
"""
Script to create an ops user for testing the Secure File Sharing API
"""

import asyncio
from app.db.mongo import db
from app.utils.auth_utils import hash_password

async def create_ops_user():
    """Create an ops user for testing"""
    email = "ops@example.com"
    password = "opspass123"
    
    # Check if user already exists
    existing = await db.users.find_one({"email": email})
    if existing:
        print(f"User {email} already exists")
        return
    
    # Create ops user
    hashed_pw = hash_password(password)
    await db.users.insert_one({
        "email": email,
        "password": hashed_pw,
        "role": "ops",
        "verified": True  # Ops users don't need email verification
    })
    
    print(f"✅ Ops user created: {email}")
    print(f"Password: {password}")

if __name__ == "__main__":
    asyncio.run(create_ops_user()) 