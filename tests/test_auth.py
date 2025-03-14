import pytest


name, email, password = "Kyrylo Test", "user@example.com", "1234"
API_URL = "/api/v1/jwt/auth"

@pytest.fixture(scope="session")
async def register_user(ac):
    response = await ac.post(
        url=API_URL + "/signup/",
        json={
            "name": name,
            "email": email,
            "password_hash": password
        }
    )
    assert response.status_code == 201
    data = response.json()

    assert "user" in data

    user_data = data["user"]

    assert isinstance(user_data, dict)
    assert "user_id" in user_data
    assert "name" in user_data
    assert "email" in user_data
    assert "password_hash" in user_data

    assert user_data["name"] == name
    assert user_data["email"] == email
    assert user_data["user_id"] > 0
    assert user_data["password_hash"] == password

    return user_data


@pytest.fixture(scope="function")
async def login_user(register_user, ac):
    response = await ac.post(
        url=API_URL + "/login/",
        data={
            "username": register_user["email"],
            "password": password
        }
    )
    assert response.status_code == 200
    reponse_json = response.json()
    assert all(token in reponse_json for token in ["access_token", "token_type", "refresh_token"]) 
    return reponse_json
