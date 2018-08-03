from flask_wtf import FlaskForm
from wtforms import SubmitField, DateField, RadioField
from wtforms.validators import DataRequired

class DatePicker(FlaskForm):
	dt_mulai = DateField('Hari Mulai', format='%Y-%m-%d', validators=[DataRequired()], render_kw={"placeholder": "YYYY-MM-DD"})
	dt_selesai = DateField('Hari Selesai', format='%Y-%m-%d', validators=[DataRequired()], render_kw={"placeholder": "YYYY-MM-DD"})
	submit = SubmitField('Submit')

class DatePickerSpecified(FlaskForm):
	start_dt = DateField('Detil Mulai', format='%Y-%m-%d %H:%M:%S', validators=[DataRequired()], render_kw={"placeholder": "YYYY-MM-DD HH:MM:SS"})
	end_dt = DateField('Detil Selesai', format='%Y-%m-%d %H:%M:%S', validators=[DataRequired()], render_kw={"placeholder": "YYYY-MM-DD HH:MM:SS"})
	submit = SubmitField('Submit')

class DropSubmit(FlaskForm):
	keep = RadioField('Drop Duplicates', choices = [('first','Keep First'),('last','Keep Last')])
	submit = SubmitField('Drop Data ')