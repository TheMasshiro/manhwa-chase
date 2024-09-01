import logging

import psycopg2
import psycopg2.errors
import psycopg2.extras
from flask import current_app, flash
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app import login


def get_db_connection():
    with current_app.app_context():
        conn = psycopg2.connect(
            host=current_app.config["HOST"],
            database=current_app.config["DATABASE"],
            port=5432,
            user=current_app.config["USER"],
            password=current_app.config["PASSWORD"],
        )
    return conn


@login.user_loader
def load_user(user_id):
    user = User(user_id=user_id)
    print(user)  # Debugging line
    return user.get_user("user_id")


class User(UserMixin):
    def __init__(
        self, username=None, email=None, password_hash=None, user_id=None
    ) -> None:
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.user_id = user_id

    def __repr__(self):
        return (
            f"<User user_id={self.user_id} username={self.username} email={self.email}>"
        )

    def get_id(self):
        """Returns the unique identifier of the user"""
        return str(self.user_id)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_user(self, identifier_type="username"):
        """Get user data based on the initialized attributes.
        Args:
            identifier_type (str): The type of identifier used (default: "username").
        Returns:
            User: A User object if found, None otherwise.
        Raises:
            ValueError: If an invalid identifier_type is provided.
        """
        allowed_identifiers = ["username", "user_id", "email"]
        if identifier_type not in allowed_identifiers:
            raise ValueError(
                f"Invalid identifier_type. Must be one of {allowed_identifiers}"
            )

        identifier = getattr(self, identifier_type, None)
        if identifier is None:
            logging.error(f"{identifier_type} is not set in the User instance.")
            return None

        query = f"SELECT * FROM users WHERE {identifier_type} = %s"

        try:
            with get_db_connection() as conn:
                with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
                    cur.execute(query, (identifier,))
                    user_data = cur.fetchone()
                    if user_data:
                        user = User(
                            username=user_data["username"],
                            email=user_data["email"],
                            password_hash=user_data["password_hash"],
                            user_id=user_data["user_id"],
                        )
                        return user
                    return None
        except psycopg2.DatabaseError as e:
            logging.error(e)
            flash("An error has occurred", "danger")
            return None
        except Exception as e:
            logging.error(e)
            flash("An error has occurred", "danger")
            return None

    def create_user(self) -> bool:
        """Create a new user.
        Returns:
            bool: `True` if the user was created successfully, `False` otherwise.
        Raise:
            UniqueViolation: Ensure the username/email is unique.
        """

        query = "INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)"

        try:
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        query,
                        (self.username, self.email, self.password_hash),
                    )
                    conn.commit()
            return True
        except psycopg2.errors.UniqueViolation as e:
            logging.error(e)
            return False
        except Exception as e:
            logging.error(e)
            return False

    def delete_user(self) -> bool:
        query = "DELETE FROM users WHERE username = %s AND email = %s"

        try:
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(query, (self.username, self.email))
                    conn.commit()
            return True
        except Exception as e:
            logging.error(e)
            return False

    def update_user(self):
        """
        Not Implemented yet
        """
        return None
