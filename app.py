from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Configuring SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chat.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Chat message model
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    content = db.Column(db.String(500), nullable=False)

# Routes
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["GET", "POST"])
def chat():
    if request.method == "POST":
        username = request.form["username"]
        content = request.form["content"]
        new_msg = Message(username=username, content=content)
        db.session.add(new_msg)
        db.session.commit()
        return redirect(url_for("chat"))
    
    messages = Message.query.order_by(Message.id.desc()).all()
    return render_template("chat.html", messages=messages)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/register")
def register():
    return render_template("register.html")

# Run the app
if __name__ == "__main__":
    # Create the database if it doesn't exist
    with app.app_context():
        db.create_all()
    
    # Bind to PORT for Render deployment
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)