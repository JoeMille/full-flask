from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_pymongo import PyMongo
from pymongo import MongoClient
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash 

app = Flask (__name__)
app.secret_key = 'mysecretkey'
app.config["MONGO_URI"] = "mongodb+srv://chefjoemiller1992:Password@cluster0.oydtt0h.mongodb.net/myDatabase?tls=true&tlsAllowInvalidCertificates=true"
mongo = PyMongo(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, id, username):
        self.id = id
        self.username = username 

users = {'Joe': {'password': '12345'}}

@login_manager.user_loader
def load_user(user_id):
    users = mongo.db.users
    user_data = users.find_one({'_id': ObjectId(user_id)})
    if user_data:
        return User(id=str(user_data['_id']), username=user_data['username'])
    return None

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'username': request.form['username']})

        if existing_user is None:
            hashpass = generate_password_hash(request.form['password'])
            users.insert_one({'username': request.form['username'], 'password': hashpass})
            return 'User created! Please login.'
        else:
            return 'Username taken! try again or login'
    
    return render_template('register.html')
   

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        users = mongo.db.users
        user_login = users.find_one({'username': request.form['username']})

        if user_login:
            if check_password_hash(user_login['password'], request.form['password']):
                user_obj = User(id=str(user_login['_id']), username=user_login['username'])
                login_user(user_obj)
                return redirect(url_for('dashboard'))
        
        return 'Invalid, try again or register'

    return render_template('index.html')

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        store_post(title, content)
        return redirect(url_for('dashboard'))
    else:
        all_posts = posts.find()
        return render_template('index.html', posts=all_posts)

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    if request.method == 'POST':
        posts = mongo.db.posts
        posts.insert_one({'title': request.form['title'], 'content': request.form['content'], 'author': current_user.username})
        return redirect(url_for('dashboard'))

    posts = mongo.db.posts.find()
    return render_template('dashboard.html', posts=posts)

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['blog_database']
posts = db['posts']

@app.route('/delete_post/<post_id>', methods=['POST'])
@login_required
def delete_post(post_id):
    post = mongo.db.posts.find_one({'_id': ObjectId(post_id)})

    if post['author'] == current_user.username:
        mongo.db.posts.delete_one({'_id': ObjectId(post_id)})
        return redirect(url_for('dashboard'))
    else:
        # Redirect to dashboard or display an error message
        return redirect(url_for('dashboard'))

def store_post(title, content):
    post_data = {
        'title': title,
        'content': content
    }
    posts.insert_one(post_data)

if __name__ == '__main__':
    app.run(debug=True)