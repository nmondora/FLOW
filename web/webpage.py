from flask import Flask, redirect, url_for, render_template

app = Flask(__name__)

# Define the home page of your site
@app.route("/")
def home():
    return render_template("start.html")

# Defining the home page of our site
@app.route("/<name>")
def user(name):
    return f"Hello {name}!"


if __name__ == "__main__":
    app.run()