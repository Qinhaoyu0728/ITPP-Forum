from flask import Flask, render_template, request

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

#from flask_bootstrap import Bootstrap

# Flask-Login需要一个UserMixin的子类
class User(UserMixin):
    def __init__(self, id, username, password, email):
        self.id = id
        self.username = username
        self.password = password
        self.email = email
        # self.is_active = True

        @property
        def is_active(self):
            return True

app = Flask(__name__)
app.secret_key = 'your secret key'

#bootstrap = Bootstrap(app)

login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = 'login'

# 用户数据
users = {'Mike': User('Mike', 'Mike', 'admin@123', 'admin@example.com'),
         'Admin': User('Admin', 'Administrator', 'admin@123', 'admin@example.com')}

@login_manager.user_loader
def load_user(user_id):
    return users.get(user_id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_id = request.form['username']
        password = request.form['password']
        remember = True if request.form.get('remember') else False

        user = load_user(user_id)
        if user and user.password == password:
            login_user(user, remember=remember)
            return redirect('/')
        else:
            # return redirect("/login")
            # return 'Invalid username or password'
            login_message = 'Invalid username or password'
            return render_template('login.html', message=login_message)
    return render_template('login.html')



@app.route('/logout')
@login_required
def logout():
    logout_user()  # 注销用户
    return redirect(url_for('home'))  # 注销后返回首页

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')  # 受保护的仪表板页面

@app.route('/')
def home():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)