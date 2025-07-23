from flask import Flask, render_template, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'emmanuel_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chat.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(500), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# Routes
@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('chat'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()
        if username and password:
            existing_user = User.query.filter_by(username=username).first()
            if existing_user:
                return "Username already exists!"
            user = User(username=username, password=password)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session['username'] = user.username
            return redirect(url_for('chat'))
        return "Invalid username or password"
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        content = request.form['message'].strip()
        if content:
            msg = Message(sender=session['username'], content=content)
            db.session.add(msg)
            db.session.commit()
    messages = Message.query.order_by(Message.timestamp.asc()).all()
    return render_template('chat.html', messages=messages, user=session['username'])

# Create the database
if __name__ == '__main__':
    if not os.path.exists('chat.db'):
        with app.app_context():
            db.create_all()
            print("✔️ chat.db created.")
    app.run(debug=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
