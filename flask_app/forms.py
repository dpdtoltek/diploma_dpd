from wtforms import Form, StringField, PasswordField, SubmitField, IntegerField, validators


class UserRegister(Form):
    username = StringField('Username', validators=[validators.DataRequired()])
    password = PasswordField('Password', validators=[validators.DataRequired()])
    repeat_password = PasswordField('Repeat password', validators=[validators.DataRequired()])
    age = IntegerField('Age', validators=[validators.DataRequired()])
    submit = SubmitField('Submit')
