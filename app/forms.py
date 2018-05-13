from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField,TextField
from wtforms.validators import DataRequired,EqualTo,ValidationError,Email,Length
from app.model import User


class LoginForm(FlaskForm):
    name = StringField(label="Username",validators=[DataRequired()])
    pwd = PasswordField(label="Password", validators=[DataRequired()])
    remember_me = BooleanField(label="Remember Me")
    submit = SubmitField(label="Sign In")


class UserRegistrationForm(FlaskForm):
    name = StringField(label="Username", validators=[DataRequired()])
    email = StringField(label="Email",validators=[DataRequired(),Email()])
    pwd = PasswordField(label="Password", validators=[DataRequired()])
    pwd2 = PasswordField(label="Re-enter Password", validators=[DataRequired(),EqualTo('pwd')])
    submit = SubmitField(label="Sign Up")

    def validate_name(self,name):
        user = User.query.filter_by(name=name.data).first()
        if user is not None:
            raise ValidationError('Plz use a different Username')

    def validate_email(self,email):
        email = User.query.filter_by(email=email.data).first()
        if email is not None:
            raise ValidationError('Plz use a different email address')


class EditProfileForm(FlaskForm):
    name = StringField('Username',validators=[DataRequired()])
    about_me = StringField(label='About Me : ',validators=[Length(min=0, max=140)] )
    submit = SubmitField('Submit')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_name(self, name):
        if name.data != self.original_username:
            user = User.query.filter_by(name=self.name.data).first()
            print(user)
            if user is not None:
                raise ValidationError('Please use a different username.')
