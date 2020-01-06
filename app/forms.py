from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
	number = StringField('Номер телефона', validators=[DataRequired()])
	email = StringField('Email', validators=[DataRequired(), Email()])
	passwd = PasswordField('Пароль', validators=[DataRequired()])
	password2 = PasswordField(
		'Повторите пароль', validators=[DataRequired(), EqualTo('passwd')])
	submit = SubmitField('Зарегистрироваться')		
    # Проверка на существование логина и email пользователя в базе данных   

	def validate_login(self, login):
		user = User.query.filter_by(login=login.data).first()
		if user is not None:
			raise ValidationError('Данный логин уже используется другим пользователем.')

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user is not None:
			raise ValidationError('Данный e-mail уже используется другим пользователем.')

class CompanyForm(FlaskForm):
	Name = StringField('Название', validators=[DataRequired()])
	URL = SelectField('Сайт', validators=[DataRequired()])
	Keyphrase = SelectField('Ключевые фразы', validators=[DataRequired()])
	Subject = SelectField(u'Предметная область', validators=[DataRequired()])
	Resoursename = SelectField('Дополнительные источники', validators=[DataRequired()])
	Resourseurl = SelectField('Сайт', validators=[DataRequired()])
	Competitorname = SelectField('Конкуренты', validators=[DataRequired()])
	Competitorurl = SelectField('Сайт', validators=[DataRequired()])
	submit = SubmitField('Отправить')	
