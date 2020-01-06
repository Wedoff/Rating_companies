from app import db
from app import db, login
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(255))
    phone = db.Column(db.String(255))
    password = db.Column(db.String(255), nullable = False)

    def __init__(self, email, phone, password):
        self.email = email
        self.phone = phone
        self.password = password

    def __repr__(self):
        return '<User {}>'.format(self.id)

    def get_id(self):
        return self.id


class Company(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    url = db.Column(db.String(255))
    subject_area = db.Column(db.String(255))
    user = db.relationship('User')

    def __init__(self, user_id, name, url, subject_area):
        self.user_id = user_id
        self.name = name
        self.url = url
        self.subject_area = subject_area

    def __repr__(self):
        return '<Company {}>'.format(self.name)


class Competitor(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    name = db.Column(db.String(255))
    url = db.Column(db.String(255))
    company = db.relationship('Company')

    def __init__(self, company_id, name, url):
        self.company_id = company_id
        self.name = name
        self.url = url

    def __repr__(self):
        return '<Competitor {}>'.format(self.url)


class Resourse(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    name = db.Column(db.String(255))
    url = db.Column(db.String(255))
    company = db.relationship('Company')

    def __init__(self, company_id, name, url):
        self.company_id = company_id
        self.name = name
        self.url = url

    def __repr__(self):
        return '<Resourse {}>'.format(self.url)


class Keyphrase(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    keyphrase = db.Column(db.String(255))
    company = db.relationship('Company')

    def __init__(self, company_id, keyphrase):
        self.company_id = company_id
        self.keyphrase = keyphrase

    def __repr__(self):
        return '<Keyphrase {}>'.format(self.keyphrase)

@login.user_loader
def load_user(id):
	if User.query.get(int(id)):
		return User.query.get(int(id))
