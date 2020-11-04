from flask import render_template,request,redirect,url_for,abort
from . import main
from .forms import BlogForm,UpdateProfileForm
from ..models import User,Comment,Blog                      
from flask_login import login_required,current_user
from .. import db



# Views
@main.route('/')
def index():
  
    '''
    View root page function that returns the index page and its data
    '''
    
    
    title = 'Welcome'
    productblog = Blog.query.filter_by(category = "productblog")
    return render_template('index.html', title = title,productblog=productblog)

@main.route('/bloges/new/', methods = ['GET','POST'])
@login_required
def new_blog():
    form = BlogForm()
    # my_updates = Update.query.filter_by(blog_id = blog.id)
    if form.validate_on_submit():
        description = form.description.data
        title = form.title.data
        user_id = current_user
        category = form.category.data
        print(current_user._get_current_object().id)
        new_blog = Blog(user_id =current_user._get_current_object().id, title = title,description=description,category=category)
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
@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():

        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)

@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))

@main.route('/delete_blog/<int:blog_id>',methods= ['POST','GET'])
@login_required
def delete_blog(blog_id):
  blog= blog.query.filter_by(id = blog_id).first()
  comments=blog.comments
  if blog.comments:
    for comment in comments:
        db.session.delete(comment)
        db.session.commit()
  user = current_user
  db.session.delete(post)
  db.session.commit()
  return redirect(url_for('main.index'))
  return render_template('index.html', user=user)

