from flask import Flask, redirect, url_for, render_template, request

app = Flask(__name__)

# Define the home page
@app.route("/")
def home():
    return render_template("start.html")

# Defining the fanno flow page
@app.route("/fanno", methods=["POST", "GET"])
def fanno():
    if request.method == "POST":
        fluid = request.form["fluid"]
        gamma = request.form["gamma"]
        tubeDiam = request.form["tubeDiam"]
        tubeLen = request.form["tubeLen"]
        frictionCoeff = request.form["frictionCoeff"]
        standardVolFlow = request.form["standardVolFlow"]
        massFlow = request.form["massFlow"]
        upstreamMach = request.form["upstreamMach"]
        upstreamVel = request.form["upstreamVel"]
        upstreamPress = request.form["upstreamPress"]
        upstreamTemp = request.form["upstreamTemp"]

        return render_template("fanno.html", fluid=fluid, gamma=gamma, tubeDiam=tubeDiam,
                               tubeLen=tubeLen, frictionCoeff=frictionCoeff, standardVolFlow=standardVolFlow,
                               massFlow=massFlow, upstreamMach=upstreamMach, upstreamVel=upstreamVel,
                               upstreamPress=upstreamPress, upstreamTemp=upstreamTemp)
    else:
        fluid = ""
        gamma = ""
        tubeDiam = ""
        tubeLen = ""
        frictionCoeff = ""
        standardVolFlow = ""
        massFlow = ""
        upstreamMach = ""
        upstreamVel = ""
        upstreamPress = ""
        upstreamTemp = ""

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