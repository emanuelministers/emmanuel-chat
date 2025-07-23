from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Config SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chat.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Model
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    content = db.Column(db.String(500), nullable=False)

# Home Page
@app.route("/")
def home():
    return render_template("index.html")

# Register Page
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Placeholder logic — store/register user (optional extension)
        username = request.form["username"]
        password = request.form["password"]
        return redirect(url_for("login"))
    return render_template("register.html")

# Login Page
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        return redirect(url_for("chat", username=username))
    return render_template("login.html")

# Chat Page
@app.route("/chat/<username>", methods=["GET", "POST"])
def chat(username):
    if request.method == "POST":
        content = request.form["content"]
        new_msg = Message(username=username, content=content)
        db.session.add(new_msg)
        db.session.commit()
        return redirect(url_for("chat", username=username))

    messages = Message.query.order_by(Message.id.desc()).limit(50).all()
    return render_template("chat.html", username=username, messages=messages)

# About Page
@app.route("/about")
def about():
    return render_template("about.html")

# Setup DB and Run App
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)