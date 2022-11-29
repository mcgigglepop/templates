from app.models import User

class RegistrationValidation():
    def validate_username(self, username):
        user = User.query.filter_by(username=username).first()
        if user is not None:
            return 'This username already exists. Please use a different username.'

    def validate_email(self, email):
        user = User.query.filter_by(email=email).first()
        if user is not None:
            return 'This email address already exists. Please use a different email address.'