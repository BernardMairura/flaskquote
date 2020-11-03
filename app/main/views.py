from flask import render_template,request,redirect,url_for,abort
from .import main
from .forms import CommentForm,BlogForm
from ..models import User,Role,Blog,Comment
from flask_login import login_required,current_user


#views

@main.route('/', methods = ['GET','POST'])
def index():

    '''
    View root page function that returns the index page and its data
    '''
    blog = blog.query.filter_by().first()
    title = 'Home'
    

    return render_template('home.html', title = title, blog = blog)
