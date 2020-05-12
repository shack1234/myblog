from . import db 
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager
from datetime import datetime 

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# creating a class for user and users table
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255),unique=True,index = True) 
    email = db.Column(db.String(255),unique = False,index = True)
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    pass_secure = db.Column(db.String(255))
        
    blog = db.relationship('Blog', backref='user', lazy='dynamic')
    comment = db.relationship('Comment', backref='user', lazy='dynamic')
    
    
    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)

    def verify_password(self,password):
            return check_password_hash(self.pass_secure, password)
    
    def save(self):
        db.session.add(self)
        db.session.commit()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f'User {self.username}'

# creating a role for users e.g the admin, superadmin extra in the table roles
class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(255))
    users = db.relationship('User',backref = 'role',lazy="dynamic") 

    def __repr__(self):
        return f'User {self.name}' 

# creating a class for the blog  and defining attribute in the table blogs
class Blog(db.Model):
    
    __tablename__ = 'blogs'
    
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(255),nullable=False)
    blogc= db.Column(db.Text(),nullable=False)
    posted = db.Column(db.DateTime,default=datetime.utcnow)
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
    comment = db.relationship('Comment', backref='blog', lazy='dynamic')

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def get_blog(id):
        blog = Blog.query.filter_by(id=id).first()

        return blog

    def __repr__(self):
        return f'Blog {self.title}'
# creating a subscribers table 
class Subscriber(db.Model):
    
    __tablename__='subscribers'

    id=db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(255),unique=True,index=True)
    def save_subscriber(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f'Subscriber {self.email}'


# creating a class for comment  and a table for comments
class Comment(db.Model):
    
    __tablename__='comments'

    id = db.Column(db.Integer,primary_key = True)
    comment = db.Column(db.String)
    posted = db.Column(db.DateTime,default=datetime.utcnow)
    blog_id = db.Column(db.Integer,db.ForeignKey("blogs.id"))
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.remove(self)
        db.session.commit()

    def get_comment(id):
        comment = Comment.query.all(id=id)
        return comment


    def __repr__(self):
        return f'Comment {self.comment}'
