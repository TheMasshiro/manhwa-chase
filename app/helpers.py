import logging

import requests
from flask import current_app, request


def recaptcha_key(key_type="public") -> str:
    if key_type == "private":
        return current_app.config["RECAPTCHA_PRIVATE_KEY"]
    return current_app.config["RECAPTCHA_PUBLIC_KEY"]


def verify_user() -> bool:
    RECAPTCHA_API = "https://www.google.com/recaptcha/api/siteverify"
    secret_key = recaptcha_key("private")

    secret_response = request.form.get("g-recaptcha-response")
    if not secret_response:
        return False

    try:
        verify_response = requests.post(
            url=RECAPTCHA_API,
            data={"secret": secret_key, "response": secret_response},
        ).json()

        if not verify_response.get("success") and verify_response.get("score", 0) < 0.5:
            return False
        return True
    except requests.RequestException as e:
        logging.error(f"reCAPTCHA verification failed: {e}")
        return False
