from dotenv import load_dotenv

import os
from flask import Flask, render_template, request, redirect, url_for, Response, flash, Response
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from datetime import datetime
from werkzeug.utils import secure_filename
from flask_migrate import Migrate

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SECRET_KEY"] = '2f6ab066798fd31d418a9b82'
load_dotenv()


db = SQLAlchemy(app)
login_manager = LoginManager(app)

@app.route('/')
def index():
    from models import Post, Img
    posts =Post.query.order_by(Post.date_posted.desc()).all()
    # img = Img.query.all()
    return render_template('index.html', posts =posts)

@app.route('/comments/<int:post_id>/', methods=('GET', 'POST'))
def postComments(post_id):
    from models import Post, Comment
    post= Post.query.get_or_404(post_id)
    if request.method=="POST":
        postComment =request.form.get('comments')
        comment = Comment(content=postComment, post= post )
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('post', post_id=post.id))
    return render_template('post.html', post=post)

# @app.route('/<int:id>')
# def get_img(id):
#     from models import Img
#     img= Img.query.filter_by(id=id).first()
#     if not img:
#         return 'no image with that id', 404
#     return Response(img.img, mimetype=img.mimetype)

#  <h3 class="title">{{ post.title }}</h3> -->
#                     <!-- <div class="imgages row"><img src="{{url_for('get_img', id=img.id)
#                     }}" alt="logo"></div> 

@app.route('/post/<int:post_id>', methods=('GET', 'POST'))
def post(post_id):
    from models import Post, Img
    post= Post.query.get_or_404(post_id)
    # img = Img.query.get_or_404(img_id)
    return render_template('post.html', post=post )


@app.route('/comments/')
@login_required
def comments():
    from models import Comment
    comments = Comment.query.order_by(Comment.id.desc()).all()
    return render_template("comments.html", comments=comments)


@app.route('/create_post/', methods=('GET', 'POST'))
@login_required
def create_post():
    from models import Post, Img
    if request.method == 'POST':       
        # pic = request.files['pic']
        # filename = secure_filename(pic.filename)
        # mimetype = pic.mimetype
        title = request.form.get('title')
        date_posted = datetime.now()
        description = request.form.get(   'description')
        author= request.form.get('author')
        new_post= Post(title=title, content=description, author= author, date_posted=date_posted)
        # newImg = Img(img=pic.read(), mimetype=mimetype, name=filename)
        db.session.add(new_post)
        # db.session.add(newImg)
        db.session.commit()
        return redirect(url_for('index' ))
    return render_template('create_post.html')

@app.route('/about/')
def about():
    return render_template('about.html')

@app.route('/contact/')
def contact():
    return render_template('contact.html')



@app.route('/register/', methods=('GET', 'POST'))
def register():
    from models import User
    if request.method == 'POST':
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        userExist= User.query.filter_by(username=username).first()
        if userExist:
            flash('Username is already taken', "error")
            return redirect(url_for("register"))

        emailExist= User.query.filter_by(email=email).first()
        if emailExist:
            flash(' email already exist', "error")

            return redirect(url_for("register"))
        passwordharsh = generate_password_hash(password)
        new_user = User(firstname = firstname, lastname=lastname, username=username, email=email, password_hash=passwordharsh ) 
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('index'))

    return render_template('register.html')


@login_manager.user_loader
def user_loader(id):
    from models import User
    return  User.query.get_or_404(int(id))

@app.route('/login/', methods=('GET', 'POST'))
def login():
    from models import User
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # user_d =
        old_user = User.query.filter_by(username=username).first()
        if old_user and check_password_hash(old_user.password_hash, password):
            login_user(old_user)
        else:
            flash("Incorrect username or password ")
            return redirect(url_for('login'))
        return redirect(url_for('index'))
    return render_template('login.html')



@app.route('/logout/', methods=('GET', 'POST'))
def logout():
    logout = logout_user()
    flash('you have successfully logged out. Login to write a blog post or make a comment on any post', 'info')
    return redirect(url_for('login'))



@app.route('/editpost/<int:pid>', methods=('GET', 'POST'))
@login_required
def editpost(pid):
    from models import Post, Img
    post_id = Post.query.get_or_404(pid)
    # img_id= Img.query.get_or_404(pic_id)
    if request.method== 'POST':
        pic = request.files['pic']
        if not pic:
            oldpic= request.form.get('src')
            pic = oldpic
        title = request.form.get('title')
        content = request.form.get('description')
        filename = secure_filename(pic.filename)
        mimetype = pic.mimetype
        # img_id.img= pic.read()
        # img_id.mimetype=mimetype
        # img_id.name=filename
        post_id.title = title
        post_id.content = content 
        db.session.add(post_id)
        # db.session.add(img_id)
        db.session.commit()
        return redirect(url_for('post', post_id=pid))
    return render_template('edit.html', post = post_id )


# @app.post('/post/<int:post_id>/delete')
# @login_required
# def delete_post(post_id):
#     from models import Post
#     post = Post.query.get_or_404(post_id)
#     db.session.delete(post)
#     db.session.commit()
#     return redirect(url_for('index'))


@app.post('/comments/<int:comment_id>/delete')
@login_required
def delete_comment(comment_id):
    from models import Comment
    comment = Comment.query.get_or_404(comment_id)
    post_id = comment.post.id
    db.session.delete(comment)
    db.session.commit()
    return redirect(url_for('post', post_id=post_id))


if __name__ == '__main__':
    app.run(debug=True, port=8000)

