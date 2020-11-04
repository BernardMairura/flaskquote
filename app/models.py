from .import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from sqlalchemy import func
from datetime import datetime
from .import login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model,UserMixin):
    __tablename__ ='users'

    id=db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(255))
    email = db.Column(db.String(255),unique = True,index = True)
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
    pass_secure = db.Column(db.String(255))
    blog = db.relationship('Blog', backref='user', lazy='dynamic')
    comment = db.relationship('Comment', backref = 'user', lazy = 'dynamic')


    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)


    def verify_password(self,password):
        return check_password_hash(self.pass_secure,password)


class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(255))
    users = db.relationship('User',backref = 'role',lazy="dynamic")


    def __repr__(self):
        return f'User {self.name}'


class Blog(db.Model):

    __tablename__ ='blogs'

    id = db.Column(db.Integer, primary_key = True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)
    description = db.Column(db.String(), index = True)
    category=db.Column(db.String(255),nullable=False)
    title = db.Column(db.String())
    comments = db.relationship('Comment',backref='blog',lazy='dynamic')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


    def save_blog(self):
        db.session.add(self)
        db.session.commit()
    @classmethod
    def get_bloges(cls,id):
        blogs = Blog.query.filter_by(blog_id=id).all()
        return bloges
    def delete_post(self):
       db.session.delete(self)
       db.session.commit()
    
    def __repr__(self):
        return f'blog {self.description}'


class Comment(db.Model):
    __tablename__='comments'
    
    id = db.Column(db.Integer,primary_key=True)
    blog_id = db.Column(db.Integer, db.ForeignKey('blogs.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable= False)
    description = db.Column(db.Text)

    
    def __repr__(self):
        return f"Comment : id: {self.id} comment: {self.description}"
    


