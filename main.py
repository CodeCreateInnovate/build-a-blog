from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['DEBUG'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:12345@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(1200))

    def __init__(self, title, body):
        self.title = title
        self.body = body


    def is_valid(self):
        if self.title and self.body:
            return True
        else:
            return False

@app.route('/')
def index():
    return redirect('/blog')

@app.route('/blog')
def blog_index():
    blog_id = request.args.get('id')
    blogs = Blog.query.all()

    if blog_id:
        post = Blog.query.get(blog_id)
        blog_title = post.title
        blog_body = post.body
        return render_template('newPosts.html', title="Blog Entry #" + blog_id, blog_title=blog_title, blog_body=blog_body)
    return render_template('blog.html', title="Build A Blog", blogs=blogs)

@app.route('/post')
def new_post():
    return render_template('post.html', title="Add New Blog Entry")

@app.route('/post', methods=['POST'])
def verify_post():
    blog_title = request.form['title']
    blog_body = request.form['body']
    title_error = ''
    body_error = ''

    if blog_title == "":
        title_error = "Title required."
    if blog_body == "":
        body_error = "Content required."

    if not title_error and not body_error:
        new_blog = Blog(blog_title, blog_body)
        db.session.add(new_blog)
        db.session.commit()
        blog = new_blog.id
        return redirect('/blog?id={0}'.format(blog))
    else:
        return render_template('post.html', title="Add New Blog Entry", blog_title = blog_title, blog_body = blog_body, title_error = title_error, body_error = body_error)

if __name__ == '__main__':
    app.run()
