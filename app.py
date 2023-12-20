from flask import Flask, render_template, request
from .calculators import fannoFlow
from pint import UnitRegistry
u = UnitRegistry()
Q_ = u.Quantity

app = Flask(__name__, template_folder='web/templates')

# Define the home page
@app.route("/")
def home():
    return render_template("home.html")

# Defining the fanno flow page
@app.route("/fanno", methods=["POST", "GET"])
def fanno():
    if request.method == "POST":
        fluid = request.form["fluid"]
        gamma = request.form["gamma"]
        tubeDiam = request.form["tubeDiam"]
        tubeLen = request.form["tubeLen"]
        frictionCoeff = request.form["frictionCoeff"]
        upstreamMach = request.form["upstreamMach"]
        upstreamVel = request.form["upstreamVel"]
        upstreamPress = request.form["upstreamPress"]
        upstreamTemp = request.form["upstreamTemp"]

        gamma = float(gamma) if gamma else None
        tubeDiam = float(tubeDiam)*u.meter if tubeDiam else None
        tubeLen = float(tubeLen)*u.meter if tubeLen else None
        frictionCoeff = float(frictionCoeff) if frictionCoeff else None
        standardVolFlow = None
        massFlow = None
        upstreamMach = float(upstreamMach) if upstreamMach else None
        upstreamVel = float(upstreamVel)*u.meter/u.second if upstreamVel else None
        upstreamPress = float(upstreamPress)*u.pascal if upstreamPress else None
        upstreamTemp = Q_(float(upstreamTemp),u.kelvin) if upstreamTemp else None 

        downstreamMach, downstreamPress, downstreamTemp = fannoFlow.fannoFlow(u, upstreamPress=upstreamPress, 
                                                                         tubeDiam=tubeDiam, tubeLen=tubeLen,
                                                                         frictionCoeff=frictionCoeff, upstreamTemp=upstreamTemp,
                                                                         standardVolFlow=standardVolFlow, massFlow=massFlow,
                                                                         upstreamMach=upstreamMach, upstreamVel=upstreamVel, fluid=fluid)
        
        fluid = "" if fluid is None else fluid
        gamma = "" if gamma is None else gamma
        tubeDiam = "" if tubeDiam is None else tubeDiam.magnitude
        tubeLen = "" if tubeDiam is None else tubeLen.magnitude
        frictionCoeff = "" if frictionCoeff is None else frictionCoeff
        standardVolFlow = "" if standardVolFlow is None else standardVolFlow.magnitude
        massFlow = "" if massFlow is None else massFlow.magnitude
        upstreamMach = "" if upstreamMach is None else upstreamMach
        downstreamMach = "" if downstreamMach is None else downstreamMach
        upstreamVel = "" if upstreamVel is None else upstreamVel.magnitude
        upstreamPress = "" if upstreamPress is None else upstreamPress.magnitude
        downstreamPress = "" if downstreamPress is None else downstreamPress.magnitude
        upstreamTemp = "" if upstreamTemp is None else upstreamTemp.magnitude
        downstreamTemp = "" if downstreamTemp is None else downstreamTemp.magnitude

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