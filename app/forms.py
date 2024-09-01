from flask_wtf import FlaskForm
from wtforms import BooleanField, EmailField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, Length, ValidationError

from app.models import User


class LoginForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired("This field is required")]
    )
    password = PasswordField(
        "Password", validators=[DataRequired("This field is required")]
    )
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Log in")

    def validate_username(self, username):
        user = User(username=username.data).get_user()
        if user is None or not user.check_password(self.password.data):
            raise ValidationError("Incorrect Username or Password")

    def validate_password(self, password):
        user = User(username=password.data).get_user()
        if user is None or not user.check_password(self.password.data):
            raise ValidationError("Incorrect Username or Password")


class RegisterForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[
            DataRequired("This field is required"),
            Length(
                min=8,
                max=20,
                message="Username must be between 8 and 20 characters long",
            ),
        ],
    )
    email = EmailField(
        "Email",
        validators=[
            DataRequired("This field is required"),
            Email("Invalid email address"),
        ],
    )
    password = PasswordField(
        "Password",
        validators=[
            DataRequired("This field is required"),
            Length(min=8, message="Password must be at least 8 characters long"),
        ],
    )
    terms_and_conditions = BooleanField(
        "I agree to the",
        validators=[DataRequired("You must agree to terms and conditions")],
    )
    remember_me = BooleanField(default=True)

    def validate_username(self, username):
        user = User(username=username.data).get_user()
        if user is not None:
            raise ValidationError("Username is already taken")

    def validate_email(self, email):
        user = User(email=email.data).get_user("email")
        if user is not None:
            raise ValidationError("Email is already taken")
