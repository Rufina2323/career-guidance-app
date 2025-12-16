import requests
import os

BASE_URL = os.getenv("BACKEND_URL", "http://app:8080")


def register_user(payload):
    return requests.post(f"{BASE_URL}/auth", json=payload)


def login(username, password):
    return requests.post(
        f"{BASE_URL}/auth/token",
        data={"username": username, "password": password},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )


def auth_headers(token):
    return {"Authorization": f"Bearer {token}"}


def get_balance(token):
    return requests.get(f"{BASE_URL}/balance", headers=auth_headers(token))


def update_balance_admin(token, user_id, amount):
    return requests.put(
        f"{BASE_URL}/admin/balance",
        headers=auth_headers(token),
        params={"user_id": user_id},
        json={"amount": amount},
    )


def transaction_history(token):
    return requests.get(
        f"{BASE_URL}/transaction_history",
        headers=auth_headers(token),
    )


def transaction_history_admin(token, user_id):
    return requests.get(
        f"{BASE_URL}/admin/transaction_history",
        headers=auth_headers(token),
        params={"user_id": user_id},
    )


def ml_request_history(token):
    return requests.get(
        f"{BASE_URL}/ml_request_history",
        headers=auth_headers(token),
    )


def create_ml_request(token, ml_model_id, payload):
    return requests.post(
        f"{BASE_URL}/ml_request",
        headers=auth_headers(token),
        params={"ml_model_id": ml_model_id},
        json=payload,
    )


def get_prediction(token, ml_request_id):
    return requests.get(
        f"{BASE_URL}/prediction",
        headers=auth_headers(token),
        params={"ml_request_id": ml_request_id},
    )
