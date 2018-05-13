from app import db,login
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from hashlib import md5


class User(UserMixin,db.Model):
    __tablename__ = "User"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64), index=True,unique=True)
    email = db.Column(db.Integer, index=True,unique=True)
    crpwd = db.Column(db.String)
    phno = db.Column(db.BigInteger)
    posts = db.relationship('Post',backref='author',lazy="dynamic")
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return "<User {}>".format(self.name)

    def set_password(self,password):
        self.crpwd = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.crpwd,password)

    def avatar(self,size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest,size)


class Post(db.Model):
    __tablename__ = "Post"
    id = db.Column(db.Integer,primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime,index=True,default=datetime.utcnow())
    user_id = db.Column(db.Integer,db.ForeignKey('User.id'))

    def __repr__(self):
        return "<Post {}>".format(self.body)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))