import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    login_required,
    logout_user,
    current_user,
)
from flask_pymongo import PyMongo
from pymongo import MongoClient
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash


# Check if environment is local or production
if os.path.exists("env.py"):
    import env

ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME')

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')
app.config["MONGO_URI"] = os.getenv("MONGO_URI")
mongo = PyMongo(app)

# Connect to MongoDB
client = MongoClient(app.config["MONGO_URI"])
db = client["blog_database"]
posts = db["posts"]

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


# User class for login manager
class User(UserMixin):
    def __init__(self, id, username, admin):
        self.id = id
        self.username = username
        self.admin = admin



# Login manager user loader
@login_manager.user_loader
def load_user(user_id):
    users = mongo.db.users
    user_data = users.find_one({"_id": ObjectId(user_id)})
    if user_data:
        return User(
            id=str(user_data["_id"]),
            username=user_data["username"],
            admin=user_data.get("admin", False),
        )
    return None


# register new user route
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        users = mongo.db.users
        existing_user = users.find_one({"username": request.form["username"]})

        if existing_user is None:
            hashpass = generate_password_hash(request.form["password"])
            users.insert_one(
                {
                    "username": request.form["username"],
                    "password": hashpass,
                }
            )
            return "User created! Please login."
        else:
            return "Username taken! try again or login"

    return render_template("register.html")


# login route
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        users = mongo.db.users
        user_login = users.find_one({"username": request.form["username"]})

        if user_login:
            if check_password_hash(user_login["password"], request.form["password"]):
                user_obj = User(
                    id=str(user_login["_id"]),
                    username=user_login["username"],
                    admin=user_login.get("admin", False),
                )
                login_user(user_obj)
                return redirect(url_for("dashboard"))

        return "Invalid, try again or register"

    return render_template("index.html")


# logout route and redirect to login
@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


# home route
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        store_post(title, content)
        return redirect(url_for("dashboard"))
    else:
        all_posts = posts.find()
        return render_template("index.html", posts=all_posts)


# dashboard route, requiring login authentication
@app.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    if request.method == "POST":
        posts = mongo.db.posts
        posts.insert_one(
            {
                "title": request.form["title"],
                "content": request.form["content"],
                "author": current_user.username,
            }
        )
        return redirect(url_for("dashboard"))

    posts = mongo.db.posts.find()
    return render_template("dashboard.html", posts=posts)


# edit and delete posts route
@app.route("/delete_post/<post_id>", methods=["POST"])
@login_required
def delete_post(post_id):
    posts = mongo.db.posts
    post = posts.find_one({"_id": ObjectId(post_id)})
    if post and post["author"] == current_user.username:
        posts.delete_one({"_id": ObjectId(post_id)})
        flash("Your post has been deleted!", "success")
    else:
        flash("You cannot delete this post", "danger")
    return redirect(url_for("dashboard"))


# store post function
def store_post(title, content):
    post_data = {"title": title, "content": content}
    posts.insert_one(post_data)


# edit post route
@app.route("/edit_post/<post_id>", methods=["GET", "POST"])
@login_required
def edit_post(post_id):
    posts = mongo.db.posts
    post = posts.find_one({"_id": ObjectId(post_id)})
    if post and post["author"] == current_user.username:
        if request.method == "POST":
            posts.update_one(
                {"_id": ObjectId(post_id)},
                {
                    "$set": {
                        "title": request.form["title"],
                        "content": request.form["edit-post-text-area"],
                    }
                },
            )
            flash("Your post has been updated!", "success")
            return redirect(url_for("dashboard"))
        else:
            return render_template("edit_post.html", post=post)
    else:
        flash("You cannot edit this post", "danger")
        return redirect(url_for("dashboard"))


if __name__ == "__main__":
    app.run(debug=False)
