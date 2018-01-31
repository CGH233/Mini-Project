# coding :utf-8
from flask import current_app, request, url_for
from flask_login import UserMixin, AnonymousUserMixin, current_user
from . import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

'''
class Role(db.Model)
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='roles', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name 
'''

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    usa = db.Column(db.Integer, index=True)
    usb = db.Column(db.Integer, index=True)
    userlikenum = db.Column(db.Integer, index=True)
    userwords = db.Column(db.Integer, index=True)
    storys = db.relationship('Story', backref='user', lazy='dynamic')
    storycs = db.relationship('Storyc', backref='user', lazy='dynamic')
    confirmed = db.Column(db.Boolean, default=False)

    @property
    def password(self):
        raise AttributeError('password is not readable')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id}).decode('utf-8')

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def __repr__(self):
        return '<User %r>' % self.username

class Story(db.Model):
    __tablename__ = 'storys'
    id = db.Column(db.Integer, primary_key=True)
    story = db.Column(db.Text(5000))
    title = db.Column(db.String(164), unique=True)
    likenum = db.Column(db.Integer)
    picture = db.Column(db.String(164))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    storycs = db.relationship('Storyc', backref='story', lazy='dynamic') 

    def __repr__(self):
        return '<Story %r>' % self.name

class Storyc(db.Model):
    __tablename__ = 'storycs'
    id = db.Column(db.Integer, primary_key=True)
    storyc = db.Column(db.Text(10000))
#   likenum = db.Column(db.Integer)
    story_id = db.Column(db.Integer, db.ForeignKey('storys.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<Storyc %r>' % self.name

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
