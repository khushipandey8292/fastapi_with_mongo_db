import pytest
import httpx
import uuid

BASE_URL = "http://127.0.0.1:8080"   # tumhare auth service ka port

@pytest.mark.asyncio
async def test_register_success():
    """Register success with unique email."""
    unique_email = f"user_{uuid.uuid4().hex[:6]}@example.com"
    async with httpx.AsyncClient(base_url=BASE_URL) as client: 
        response = await client.post("/auth/register", json={
            "email": unique_email,
            "name": "Test User",
            "password": "testpassword"
        })
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["email"] == unique_email


@pytest.mark.asyncio
async def test_register_existing_email():
    """Same email 2nd time → should fail with 400."""
    email = f"user_{uuid.uuid4().hex[:6]}@example.com"

    # Pehli baar register
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        await client.post("/auth/register", json={
            "email": email,
            "name": "User1",
            "password": "password123"
        })

    # Dusri baar same email
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.post("/auth/register", json={
            "email": email,
            "name": "User1",
            "password": "password123"
        })

    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"


@pytest.mark.asyncio
async def test_login_success():
    """Login with correct credentials."""
    email = f"user_{uuid.uuid4().hex[:6]}@example.com"
    password = "password123"

    # Register user
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        await client.post("/auth/register", json={
            "email": email,
            "name": "Login User",
            "password": password
        })

    # Login
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.post(
            "/auth/login",
            data={"username": email, "password": password},
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_invalid_credentials():
    """Login with wrong password → should fail with 401."""
    email = f"user_{uuid.uuid4().hex[:6]}@example.com"
    password = "password123"

    # Register user
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        await client.post("/auth/register", json={
            "email": email,
            "name": "Invalid Login User",
            "password": password
        })

    # Wrong password
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.post(
            "/auth/login",
            data={"username": email, "password": "wrongpassword"},
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"
