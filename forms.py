from flask_wtf import FlaskForm
from wtforms.widgets import NumberInput
from wtforms import StringField, PasswordField, IntegerField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo

class AuthForm(FlaskForm):
    seller_name = StringField('Nombre de usuario', validators=[DataRequired()])
    seller_pass = PasswordField('Contraseña', 
            validators=[DataRequired(),
                        Length(min=8),
                        EqualTo('confirm', message='Las contraseñas no coinciden')
                        ])
    confirm = PasswordField('Confirmar contraseña',
                        validators=[DataRequired()])
    
class ProductForm(FlaskForm):
    product_name = StringField('Nombre del producto', validators=[DataRequired()])
    product_price = IntegerField('Precio del producto', validators=[DataRequired()])
    product_desc = StringField('Descripción del producto', validators=[DataRequired()])
    product_exists = BooleanField('En existencia')

class HourForm(FlaskForm):
    start_hour = IntegerField('Hora de entrada', validators=[DataRequired()])
    leaving_hour = IntegerField('Hora de salida', validators=[DataRequired()])