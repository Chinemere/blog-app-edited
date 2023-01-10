from app import db
from flask_login import  UserMixin
from datetime import date

class Post(db.Model): 
    id = db.Column(db.Integer, primary_key= True)
    title = db.Column(db.String(300), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id', use_alter=True))
    author = db.Column(db.String(200), nullable=False)
    date_posted = db.Column(db.DateTime)
    user = db.relationship('User', backref ="post", foreign_keys=[user_id])
    comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
    


    def __repr__(self):
        return f'<Post "{self.title}">'


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    content = db.Column(db.Text())
    post_id= db.Column(db.Integer, db.ForeignKey('post.id', use_alter=True))
    post = db.relationship('Post', backref='comment', foreign_keys=[post_id])
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', use_alter=True))
    user = db.relationship('User', backref='comment', foreign_keys=[user_id])
    


    def __repr__(self) :
        return f'{self.user}: {self.content[:100]}'

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True, nullable=False)
    firstname = db.Column(db.String(200), nullable=False)
    lastname = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200),  nullable=False, unique=True)
    username = db.Column(db.String(200),  nullable=False, unique=True)
    password_hash = db.Column(db.Text,  nullable=False)

    

    def __repr__(self):
        return f'{self.username}'
    

class Img(db.Model):
    id = db.Column(db.Integer, primary_key=True )
    img =db.Column(db.Text, unique=True, nullable=False)
    name = db.Column(db.Text,  nullable=False)
    mimetype = db.Column(db.Text, nullable=False)