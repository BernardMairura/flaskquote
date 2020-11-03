from flask import render_template,request,redirect,url_for,abort
from .import main
from .forms import CommentForm,BlogForm
from ..models import User,Role,Blog,Comment
from flask_login import login_required,current_user
from .. import db
from flask.views import View,MethodView


#views

@main.route('/')
def index():

    '''
    View root page function that returns the index page and its data
    '''
    
    title = 'welcome'
    pblog = Blog.query.filter_by(category="pblog")
    

    return render_template('index.html', title = title, pblog = pblog)


@main.route('/blogs/new/', methods = ['GET','POST'])
@login_required
def new_blog():
    form = BlogForm()
    if form.validate_on_submit():
        description = form.description.data
        title = form.title.data
        owner_id = current_user
        print(current_user._get_current_object().id)
        new_blog = Blog(owner_id =current_user._get_current_object().id, title = title,description=description)
        db.session.add(new_blog)
        db.session.commit()
        
        
        return redirect(url_for('main.index'))
    return render_template('blog.html',form=form)


@main.route('/comment/new/<int:blog_id>', methods = ['GET','POST'])
@login_required
def new_comment(blog_id):
    form = CommentForm()
    blog=Blog.query.get(blog_id)
    if form.validate_on_submit():
        description = form.description.data

        new_comment = Comment(description = description, user_id = current_user._get_current_object().id, blog_id = blog_id)
        db.session.add(new_comment)
        db.session.commit()


        return redirect(url_for('.new_comment', blog_id= blog_id))

    all_comments = Comment.query.filter_by(blog_id = blog_id).all()
    return render_template('comments.html', form = form, comment = all_comments, blog = blog )