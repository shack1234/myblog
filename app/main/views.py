from flask import render_template, request, redirect, url_for, abort ,flash
from ..models import  User,Blog,Comment,Subscriber
from flask_login import login_required, current_user
from ..email import mail_message
from .forms import UpdateProfile,Blogs
from .. import db,photos
from . import main  
import markdown2
from ..request import get_quote

@main.route('/')
def index():
    '''
    View root page function that returns the index page and its data
    '''
    title = 'Home - Blog Application Page'
    blogs = Blog.query.order_by(Blog.posted.desc())
    quote = get_quote()
    
    return render_template('index.html',blogs=blogs,title=title,quote=quote)

# updating a profile picture
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

# getting a proofile picture
@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()
    title= 'Profile page'
    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user,title=title)
# updating user profile
@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    title='Update profile page'
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))
    return render_template('profile/update.html',form =form,title=title)

# creating a blog
@main.route('/new-blog', methods=['POST','GET'])
@login_required
def new_blog():
    subscribers = Subscriber.query.all()
    title='Blogs Page'
    form = Blogs()
    if form.validate_on_submit():
        title = form.title.data
        blogc = form.blogc.data
        user_id =  current_user._get_current_object().id
        blog = Blog(title=title,blogc=blogc,user_id=user_id)
        blog.save()
        for subscriber in subscribers:
            mail_message("New Blog Post","email/new_blog",subscriber.email,blog=blog)
        return redirect(url_for('main.index'))
       
    return render_template('newblog.html', form = form,title=title)

@main.route('/blog/<id>')
def blog(id):
    comments = Comment.query.filter_by(blog_id=id).all()
    blog = Blog.query.get(id)
    title="Blogs"
    return render_template('blog.html',blog=blog,comments=comments,title=title)


@main.route('/subscribe',methods = ['POST','GET'])
def subscribe():
    email = request.form.get('subscriber')
    new_subscriber = Subscriber(email = email)
    new_subscriber.save_subscriber()
    mail_message("Subscribed to Mblog","email/welcome_subscriber",new_subscriber.email,new_subscriber=new_subscriber)
    flash('Sucessfully subscribed')
    return redirect(url_for('main.index'))     

@main.route('/blog/<blog_id>/update', methods = ['GET','POST'])
@login_required
def updateblog(blog_id):
    blog = Blog.query.get(blog_id)
    title= 'Update Blog Page'
    if blog.user != current_user:
        abort(403)
    form = Blogs()
    if form.validate_on_submit():
        blog.title = form.title.data
        blog.blogc = form.blogc.data
        db.session.commit()
       
        return redirect(url_for('main.blog',id = blog.id))
     
    if request.method == 'GET':
        form.title.data = blog.title
        form.blogc.data = blog.blogc
    return render_template('newblog.html',form = form,title=title)

@main.route('/comment/<blog_id>', methods = ['Post','GET'])
@login_required
def comment(blog_id):
    blog = Blog.query.get(blog_id)
    comment =request.form.get('newcomment')
    new_comment = Comment(comment = comment, user_id = current_user._get_current_object().id, blog_id=blog_id)
    new_comment.save()
    return redirect(url_for('main.blog',id =blog.id))

@main.route('/user/<string:username>')
def user_posts(username):
    user = User.query.filter_by(username=username).first()
    blogs = Blog.query.filter_by(user=user).order_by(Blog.posted.desc())
    return render_template('view_user_post.html',blogs=blogs,user = user)


@main.route('/blog/<blog_id>/delete', methods = ['POST'])
@login_required
def delete_post(blog_id):
    blog = Blog.query.get(blog_id)
    if blog.user != current_user:
        abort(403)
    blog.delete()
    flash("You have deleted your Blog succesfully!")
    return redirect(url_for('main.index'))
