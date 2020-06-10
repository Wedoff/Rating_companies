import os
import re
import smtplib
import random
import datetime
import operator
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
	#if 'loggedin' in session:
		#return redirect('profile')
	return render_template('company.html')
	
@app.route('/login')
def fun1start():
	if 'loggedin' in session:
		return redirect('company')
	return render_template('login.html')

	
@app.route('/index')
def fun1start1():
	if 'loggedin' in session:
		return redirect('company')
	return render_template('index.html')
	
@app.route('/result', methods=['POST'])
def funres():
	if 'loggedin' in session:
		#список + коммент
		pol_emot=[]
		#список - коммент
		otr_emot=[]
		#список нейтр коммент
		net_enot=[]
		lencomfornews={}
		
		cn = request.form['companyname']
		con = mysql.connector.connect(user = 'root', password = 'KmddsjYYw34', host = '127.0.0.1', database = 'RC')
		cursor = con.cursor()
		
		#поиск новостей с упоминанием компании
		cursor.execute('SELECT name_id FROM entites WHERE value like = %(n)s', { 'n': cn })
		companys = cursor.fetchone()
		
		#для каждой новости ищем комментарии
		for i in range(0, len(companys)):
			cursor.execute('SELECT id FROM comments WHERE news_ id = %(n)s', { 'n': companys[i] })
			idcom = cursor.fetchone()
			#число комментариев для конкретной новости в виде словаря
			lencomfornews[companys[i]] = len(idcom)
			#просмотр эмоц. окраски для каждого комментария
			for j in range(0,len(idcom)):
				cursor.execute('SELECT emotional_coloring_id FROM analyzed_comments WHERE comment_id = %(n)s', { 'n': idcom[i] })
				emot=cursor.fetchone()
				if emot > 0:
					pol_emot=pol_emot.append(emot)
				if emot < 0:
					otr_emot=otr_emot.append(emot)
				if emot = 0:
					net_enot=net_enot.append(emot)
		#сортировка словаря по числу комментариев от мин к макс
		b=sorted(lencomfornews.items(),key = operator.itemgetter(1))	
		#cписок id новостей по убываю числа комметариев к ней
		for i in reversed(b):
			cursor.execute('SELECT news_header,sourse_id FROM news WHERE id = %(n)s', { 'n': b[0]})
			companysnews = cursor.fetchone()
		
		#??? как вывести источник, для 6 самых обсуждаемых новостей 
		cursor.close()
		con.close()		
		
		return render_template('result.html', companyname = cn, len = len(companys), companysnews, pol = len(pol_emot), net = len(net_enot), otr = len(otr_emot))
	else:
		return redirect('login')
	
@app.route('/profile')
def profile():,
	if 'loggedin' in session:
		con = mysql.connector.connect(user = 'root', password = 'KmddsjYYw34', host = '127.0.0.1', database = 'RC')
		cursor = con.cursor()
    
		id = session['id']
		cursor.execute('SELECT name FROM company WHERE user_id = %(n)s', { 'n': session['id'] })
		company = cursor.fetchone()
    
		print(company)
		cursor.close()
		con.close()
		
		return render_template('profile.html', len = len(c), company = company)
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
  print(_username, _password)
  
  if (_username is None) or (_password is None): return render_template('start.html', msg='Неверный ввод') 
  
  con = mysql.connector.connect(user = 'root', password = 'KmddsjYYw34', host = '127.0.0.1', database = 'RC')
  cursor = con.cursor()
  test = 'SELECT id, email FROM user WHERE email = %(n)s'
  
  cursor.execute(test, { 'n': _username })
  account = cursor.fetchone()

  if account:
    # Create session data, we can access this data in other routes
    session['loggedin'] = True
    session['id'] = account[0]
    session['username'] = account[1]
    return redirect('company')
  else:
    return render_template('login.html', msg='Неверное имя или пароль')
    
  cursor.close()
  con.close()
	
@app.route('/registerr', methods=['POST'])
@login_required
def add_company():
	if 'loggedin' in session:
		
		connection = mysql.connector.connect(user = 'root', password = 'KmddsjYYw34', host = '127.0.0.1', database = 'RC')
		cursor = connection.cursor()
		
		id = session['id']
		
		insert_company = "INSERT INTO company(user_id, name, url, subject_area)  VALUES (%s, %s, %s, %s)"
		cursor.execute(insert_company, (id, request.form['Name'], request.form['URL'], request.form['Subject']))
       
		idr = cursor.lastrowid
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
		cursor.close()
		connection.close()
	
		return redirect('/profile')
	else:
		redirect('/login')


@app.route('/logout')
def logout():
	session.pop('loggedin', None)
	session.pop('id', None)
	session.pop('username', None)
	return redirect('/login')
