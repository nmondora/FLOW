from flask import Flask, redirect, url_for, render_template, request
from .. import fannoFlow
from pint import UnitRegistry
u = UnitRegistry()
Q_ = u.Quantity

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

        gamma = float(gamma) if gamma else None
        tubeDiam = float(tubeDiam)*u.meter if tubeDiam else None
        tubeLen = float(tubeLen)*u.meter if tubeLen else None
        frictionCoeff = float(frictionCoeff) if frictionCoeff else None
        standardVolFlow = float(standardVolFlow)*u.foot**3/u.second if standardVolFlow else None
        massFlow = float(massFlow)*u.kilogram/u.meter if massFlow else None
        upstreamMach = float(upstreamMach) if upstreamMach else None
        upstreamVel = float(upstreamVel)*u.meter/u.second if upstreamVel else None
        upstreamPress = float(upstreamPress)*u.pascal if upstreamPress else None
        upstreamTemp = Q_(float(upstreamTemp),u.kelvin) if upstreamTemp else None 

        downstreamMach, downstreamPress, downstreamTemp = fannoFlow(u, fluid=fluid, upstreamPress=upstreamPress, 
                                                                         tubeDiam=tubeDiam, tubeLen=tubeLen,
                                                                         frictionCoeff=frictionCoeff, upstreamTemp=upstreamTemp,
                                                                         standardVolFlow=standardVolFlow, massFlow=massFlow,
                                                                         upstreamMach=upstreamMach, upstreamVel=upstreamVel)
        
        gamma = "" if gamma is None else gamma
        tubeDiam = "" if tubeDiam is None else tubeDiam
        tubeLen = "" if tubeDiam is None else tubeLen
        frictionCoeff = "" if frictionCoeff is None else frictionCoeff
        standardVolFlow = "" if standardVolFlow is None else standardVolFlow
        massFlow = "" if massFlow is None else massFlow
        upstreamMach = "" if upstreamMach is None else upstreamMach
        downstreamMach = "" if downstreamMach is None else downstreamMach
        upstreamVel = "" if upstreamVel is None else upstreamVel
        upstreamPress = "" if upstreamPress is None else upstreamPress
        downstreamPress = "" if downstreamPress is None else downstreamPress
        upstreamTemp = "" if upstreamTemp is None else upstreamTemp
        downstreamTemp = "" if downstreamTemp is None else downstreamTemp

        return render_template("fanno.html", fluid=fluid, gamma=gamma, tubeDiam=tubeDiam,
                               tubeLen=tubeLen, frictionCoeff=frictionCoeff, standardVolFlow=standardVolFlow,
                               massFlow=massFlow, upstreamMach=upstreamMach, downstreamMach=downstreamMach, upstreamVel=upstreamVel,
                               upstreamPress=upstreamPress, downstreamPress=downstreamPress, upstreamTemp=upstreamTemp, downstreamTemp=downstreamTemp)
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