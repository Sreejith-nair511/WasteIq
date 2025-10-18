#!/usr/bin/env python3
"""
Test file to verify imports work correctly with our specified versions
"""

try:
    from fastapi import FastAPI, UploadFile, File, Form, HTTPException
    print("✓ FastAPI imports successful")
except Exception as e:
    print(f"✗ FastAPI import failed: {e}")

try:
    from pydantic import BaseModel
    print("✓ Pydantic imports successful")
except Exception as e:
    print(f"✗ Pydantic import failed: {e}")

try:
    import uvicorn
    print("✓ Uvicorn imports successful")
except Exception as e:
    print(f"✗ Uvicorn import failed: {e}")

try:
    from faker import Faker
    print("✓ Faker imports successful")
except Exception as e:
    print(f"✗ Faker import failed: {e}")

try:
    from fastapi.middleware.cors import CORSMiddleware
    print("✓ CORS middleware imports successful")
except Exception as e:
    print(f"✗ CORS middleware import failed: {e}")

print("All imports tested!")