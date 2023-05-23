from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo

class AuthForm(FlaskForm):
    username = StringField('Nombre de usuario', validators=[DataRequired()])
    password = PasswordField('Contraseña', 
            validators=[DataRequired(),
                        Length(min=8),
                        EqualTo('confirm', message='Las contraseñas no coinciden')
                        ])
    confirm = PasswordField('Confirmar contraseña',
                        validators=[DataRequired()])