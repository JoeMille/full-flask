from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user

app = Flask (__name__)
app.secret_key = 'mysecretkey'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, id):
        self.id = id

users = {'Joe': {'password': 'Torbay321'}}

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username]['password'] == password:
            user = User(username)
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            return 'Invalid username or password'
    else:
        return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return 'Logged out successfully!'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/dashboard')
@login_required 
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)