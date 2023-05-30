from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
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
    product_price = StringField('Precio del producto', validators=[DataRequired()])
    product_desc = StringField('Descripción del producto', validators=[DataRequired()])