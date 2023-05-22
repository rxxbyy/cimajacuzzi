from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo

class RegisterForm(FlaskForm):
    username = StringField('Nombre de usuario', validators=[DataRequired()])
    password = PasswordField('Nueva contraseña', 
            validators=[DataRequired(),
                        Length(min=8),
                        EqualTo('confirm', message='Las contraseñas deben coincidir')
                        ])
    confirm = PasswordField('Confirmar contraseña',
                        validators=[DataRequired()])

class LoginForm(FlaskForm):
    username = StringField('Nombre de usuario', validators=[DataRequired()])
    password = StringField('Contraseña', validators=[DataRequired()])
