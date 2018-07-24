from flask_wtf import FlaskForm
from wtforms import DateField
from wtforms.validators import DataRequired


class DatePicker(FlaskForm):
	dt_mulai = DateField('DatePicker', format='%Y-%m-%d', validators=[DataRequired()], description = 'Hari Mulai')
	dt_selesai = DateField('DatePicker', format='%Y-%m-%d', validators=[DataRequired()], description = 'Hari Selesai')
