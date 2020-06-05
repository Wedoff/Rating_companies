import os
import re
import smtplib
import random
import datetime
import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode
from flask import Flask, render_template, redirect, url_for, request, flash, session
from app import app
from app import db
from datetime import datetime
from app.forms import RegistrationForm, CompanyForm
from flask_login import current_user, login_user, logout_user, login_required, login_fresh
from app.models import User, Company, Resourse, Competitor, Keyphrase
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename
from flask import send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from email.mime.text import MIMEText
from flask_login import user_loaded_from_header, LoginManager
from flask_paginate import Pagination,  get_page_parameter,  get_page_args

@app.route('/company')
def fun1():
	#if current_user.is_authenticated:
	#	return redirect('profile')
	return render_template('company.html')
	
@app.route('/login')
def fun1start():
	if current_user.is_authenticated:
		return redirect('company')
	return render_template('login.html')

	
@app.route('/index')
def fun1start1():
	if current_user.is_authenticated:
		return redirect('company')
	return render_template('index.html')

@app.route('/result')
def funres():
	return render_template('result.html')
	
@app.route('/profile')
@login_required
def profile():
#как вывести список компаний, которые ввел один пользователь, чтобы при нажатии на компанию выходила страница с результатами именно для нее????
	if current_user.is_active:
		id = db.session.query(User.UserID).filter(User.Email == current_user.Email)
		c = db.session.query(Company.CompanyID, Company.Name).filter(Company.UserID == id).all()
		return render_template('profile.html', companys = c)
	else:
		return redirect('login')
	
@app.route('/bd')
def fun1bd():
	#if current_user.is_authenticated:
	#	return redirect('profile')
	return render_template('bd.html', users = User.query.all(), companys = Company.query.all(), resourses = Resourse.query.all(), сompetitors = Competitor.query.all(), keyphrases = Keyphrase.query.all())


@app.route('/register', methods=['GET', 'POST'])
def register():
  connection = mysql.connector.connect(user = 'root', password = 'KmddsjYYw34', host = '127.0.0.1', database = 'RC')
  cursor = connection.cursor()

  if (current_user.is_authenticated):
    return redirect('company') #если пользователь уже зашел, то переход на стр личного кабинета (company)

  form = RegistrationForm()
  if form.validate_on_submit():
    insert_user = "INSERT INTO user(email, phone, password) VALUES (%s, %s, %s)"
    cursor.execute(insert_user, (form.email.data, form.number.data, generate_password_hash(form.passwd.data)))
    connection.commit()
    cursor.close()
    connection.close()
    flash('Регистрация прошла успешно')
    return redirect('/login') #перенаправление на вход в личный кабинет
  return render_template('register.html', title='Регистрация', form=form)
	
@app.route('/log',methods=['POST'])
def fun2():
	_username = request.form.get('user')
	_password = request.form.get('pass')
	
	con = mysql.connector.connect(user = 'root', password = 'KmddsjYYw34', host = '127.0.0.1', database = 'RC')
	cursor = con.cursor()

	if (_username is None) or (_password is None): return render_template('start.html', msg='Неверный ввод') 
	f = select top 1 user from users where email = _username
	if f is None:
		return render_template('login.html', msg='Неверный логин или пароль')
	else:
		if check_password_hash(f.password_hash, _password):
			login_user(f)
			return redirect('company')
	return render_template('login.html', msg='Неверное имя или пароль')
			
	cursor.close()
	con.close()
	
@app.route('/registerr', methods=['POST'])
@login_required
def add_company():
	connection = mysql.connector.connect(user = 'root', password = 'KmddsjYYw34', host = '127.0.0.1', database = 'RC')
	cursor = connection.cursor()
	
	if current_user.is_authenticated:
		id = db.session.query(User.UserID).filter(User.Email == current_user.Email) 
		#как найти id юзера который сейчас авторизован, будет ли работать flask_login
		
		insert_company = "INSERT INTO company(user_id, name, url, subject_area)  VALUES (%s, %s, %s, %s)"
		cursor.execute(insert_company, (id, request.form['Name'], request.form['URL'], request.form['Subject']))
       
		#idr = db.session.query(Company.CompanyID).filter(Company.Name == request.form['Name'], Company.UserID == id, Company.URL == request.form['URL'], Company.Subject == request.form['Subject'])
		
		idr = SELECT IDENT_CURRENT('company') AS [IDENT_CURRENT]
		#поиск последней добавленной компании
		
		insert_resourse = "INSERT INTO resourse(company_id, url, name)  VALUES (%s, %s, %s)"
		cursor.execute(insert_resourse, (idr, request.form['Resourseurl'], request.form['Resoursename']))
		
		insert_competitor = "INSERT INTO competitor(company_id, url, name)  VALUES (%s, %s, %s)"
		cursor.execute(insert_competitor, (idr, request.form['Competitorurl'], request.form['Competitorname1']))
		insert_competitor = "INSERT INTO competitor(company_id, url, name)  VALUES (%s, %s, %s)"
		cursor.execute(insert_competitor, (idr, request.form['Competitorur2'], request.form['Competitorname2']))
		insert_competitor = "INSERT INTO competitor(company_id, url, name)  VALUES (%s, %s, %s)"
		cursor.execute(insert_competitor, (idr, request.form['Competitorur3'], request.form['Competitorname3']))
		insert_competitor = "INSERT INTO competitor(company_id, url, name)  VALUES (%s, %s, %s)"
		cursor.execute(insert_competitor, (idr, request.form['Competitorur4'], request.form['Competitorname4']))

		insert_keyphrase = "INSERT INTO keyphrase(company_id, keyphrase)  VALUES (%s, %s])"
		cursor.execute(insert_keyphrase, (idr, request.form['Keyphrases']))
		connection.commit()
	
		return redirect('/profile')
	else:
		redirect('/login')
	cursor.close()
	connection.close()

@app.route('/logout')
def logout():
 session.pop('user',None)
 return redirect('/login')
