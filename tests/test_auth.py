import pytest

from app import create_app

app = create_app()


@pytest.mark.parametrize(
    "username_register,email_register,password_register,terms,expected_message_register",
    [
        (
            "user",
            "test@example.com",
            "testpassword",
            "on",
            b"Username must be between 8 and 20 characters long",
        ),
        (
            "testusername",
            "testemail",
            "testpassword",
            "on",
            b"Invalid email address",
        ),
        (
            "testuser",
            "test@example.com",
            "test",
            "on",
            b"Password must be at least 8 characters long",
        ),
        (
            "testusername",
            "test@example.com",
            "testpassword",
            "",
            b"You must agree to terms and conditions",
        ),
        ("", "", "", "", b"This field is required"),
    ],
)
def test_register_failures(
    client,
    username_register,
    email_register,
    password_register,
    terms,
    expected_message_register,
):
    response = client.post(
        "/register",
        data={
            "username": username_register,
            "email": email_register,
            "password": password_register,
            "terms_and_conditions": terms,
        },
    )
    assert response.status_code == 200
    assert expected_message_register in response.data


def test_register_same_username(client):
    response = client.post(
        "/register",
        data={
            "username": "testusername",
            "email": "testemail2@example.com",
            "password": "testpassword",
            "terms_and_conditions": "on",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Username is already taken" in response.data


def test_register_success(client):
    response = client.post(
        "/register",
        data={
            "username": "testusername",
            "email": "testemail@example.com",
            "password": "testpassword",
            "terms_and_conditions": "on",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Welcome" in response.data


@pytest.mark.parametrize(
    "username_login,password_login,expected_message_login",
    [
        (
            "testsername",
            "wrongpassword",
            b"Incorrect Username or Password",
        ),
        ("", "", b"This field is required"),
    ],
)
def test_login_failures(
    client,
    username_login,
    password_login,
    expected_message_login,
):
    response = client.post(
        "/login",
        data={
            "username": username_login,
            "password": password_login,
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert expected_message_login in response.data


def test_login_success(client):
    response = client.post(
        "/login",
        data={
            "username": "testusername",
            "password": "testpassword",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Welcome" in response.data


def test_logout(client):
    response = client.get("/logout")
    assert response.status_code == 302
    print(response.data)
    assert b"You should be redirected automatically" in response.data
