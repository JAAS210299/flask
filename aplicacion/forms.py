from flask_wtf import FlaskForm
from wtforms import IntegerField,SelectField,SubmitField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileRequired

class formcalculadora(FlaskForm):
    num1=IntegerField("Número1",validators=[DataRequired("Tienes que introducir el dato")])
    num2=IntegerField("Número2",validators=[DataRequired("Tienes que introducir el dato")])
    operador=SelectField("Operador",choices=[("+","Sumar"), ("-", "Restar"), 
                                            ("*", "Multiplicar"), ("/", "Dividir")])
    submit = SubmitField('Submit')

class UploadForm(FlaskForm):
    photo = FileField('selecciona imagen:', validators=[FileRequired()])
    submit = SubmitField('Submit')