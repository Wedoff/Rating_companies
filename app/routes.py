#-*- coding: utf-8 -*-
import os
import re
import smtplib
import random
import datetime
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
	
@app.route('/bd')
def fun1bd():
	#if current_user.is_authenticated:
	#	return redirect('profile')
	return render_template('bd.html', users = User.query.all(), companys = Company.query.all(), resourses = Resourse.query.all(), сompetitors = Competitor.query.all(), keyphrases = Keyphrase.query.all())


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect('company') #если пользователь уже зашел, то переход на стр личного кабинета (company)
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(Email=form.email.data, Number=form.number.data, password_hash=generate_password_hash(form.passwd.data))

        db.session.add(user)
        db.session.commit()
        flash('Регистрация прошла успешно')
        return redirect('/login') #перенаправление на вход в личный кабинет
    return render_template('register.html', title='Регистрация', form=form)
	
@app.route('/log',methods=['POST'])
def fun2():
	us = request.form.get('user')
	ps = request.form.get('pass')
	if (us is None) or (ps is None): return render_template('start.html', msg='Неверный ввод')
	f = User.query.filter_by(Email=us).first()
	if f is None:
		return render_template('login.html', msg='Неверный логин или пароль')
	else:
		if check_password_hash(f.password_hash, ps):
			login_user(f)
			return redirect('company')
	return render_template('login.html', msg='Неверное имя или пароль')
	
@app.route('/registerr', methods=['POST'])
@login_required
def add_company():
	if current_user.is_authenticated:
		id = db.session.query(User.UserID).filter(User.Email == current_user.Email)
		company = Company(id, request.form['Name'], request.form['URL'], request.form['Subject'])
		db.session.add(company)
		db.session.commit() 
		idr = db.session.query(Company.CompanyID).filter(Company.Name == request.form['Name'], Company.UserID == id, Company.URL == request.form['URL'], Company.Subject == request.form['Subject'])
		resourse = Resourse(idr, request.form['Resourseurl'], request.form['Resoursename'])
		competitor = Competitor(idr, request.form['Competitorurl'], request.form['Competitorname'])
		db.session.add(competitor)	
		competitor = Competitor(idr, request.form['Competitorurl1'], request.form['Competitorname1'])
		db.session.add(competitor)	
		competitor = Competitor(idr, request.form['Competitorurl2'], request.form['Competitorname2'])
		db.session.add(competitor)	
		competitor = Competitor(idr, request.form['Competitorurl3'], request.form['Competitorname3'])
		keyphrase = Keyphrase(idr, request.form['Keyphrases'])
		db.session.add(resourse)
		db.session.add(competitor)		
		db.session.add(keyphrase)
		db.session.commit() 
		return redirect('/bd')
	else:
		redirect('/login')
		
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')