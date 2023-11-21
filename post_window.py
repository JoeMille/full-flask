# post_window.py
from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo
from flask_login import current_user

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase"  # Replace with your MongoDB URI
mongo = PyMongo(app)

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        # Get the post content from the form
        content = request.form.get('content')

        # Insert the new post into the 'posts' collection
        mongo.db.posts.insert_one({'title': 'Post by ' + current_user.id, 'content': content})

        # Redirect back to the dashboard
        return redirect(url_for('dashboard'))

    # Get all posts from the 'posts' collection
    posts = mongo.db.posts.find()

    # Render the dashboard template with the current user and posts
    return render_template('dashboard.html', current_user=current_user, posts=posts)

@app.route('/create_post', methods=['POST'])
def create_post():
    content = request.form.get('content')

    mongo.db.posts.insert_one({'title': 'Post by ' + current_user.id, 'content': content})

    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)