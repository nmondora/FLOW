from flask import Flask, redirect, url_for, render_template

app = Flask(__name__)

# Define the home page
@app.route("/")
def home():
    return render_template("start.html")

# Defining the fanno flow page
@app.route("/fanno")
def fanno():
    return render_template("fanno.html")

# Defining the rayleigh flow page
@app.route("/rayleigh")
def rayleigh():
    return render_template("rayleigh.html")

# Defining the isentropic flow page
@app.route("/isentropic")
def isentropic():
    return render_template("isentropic.html")

# Defining the fanno flow page
@app.route("/shocks")
def shocks():
    return render_template("shocks.html")


if __name__ == "__main__":
    app.run()