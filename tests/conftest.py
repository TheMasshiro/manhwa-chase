import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app
from app.models import User


@pytest.fixture()
def app():
    app = create_app()
    app.config.update(
        {
            "TESTING": True,
        }
    )

    # other setup can go here
    with app.app_context():
        user = User(username="testusername", email="testemail@example.com")
        user.set_password("testpassword")
        user.create_user()

    yield app

    # clean up / reset resources here
    with app.app_context():
        user.delete_user()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
