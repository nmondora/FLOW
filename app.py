from flask import Flask, render_template, request, jsonify
from calculators import fannoFlow, isentropicFlow
from pint import UnitRegistry
u = UnitRegistry()
Q_ = u.Quantity

app = Flask(__name__, template_folder='web/templates', static_folder='web/static')

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

        return jsonify({
            "fluid": fluid,
            "gamma": gamma,
            "tubeDiam": tubeDiam,
            "tubeLen": tubeLen,
            "frictionCoeff": frictionCoeff,
            "standardVolFlow": standardVolFlow,
            "massFlow": massFlow,
            "upstreamMach": upstreamMach,
            "downstreamMach": downstreamMach,
            "upstreamVel": upstreamVel,
            "upstreamPress": upstreamPress,
            "downstreamPress": downstreamPress,
            "upstreamTemp": upstreamTemp,
            "downstreamTemp": downstreamTemp
        })
    else:
        fluid = ""
        gamma = "1.4"
        tubeDiam = ""
        tubeLen = ""
        frictionCoeff = ""
        standardVolFlow = ""
        massFlow = ""
        upstreamMach = ""
        upstreamVel = ""
        upstreamPress = ""
        upstreamTemp = ""

        return render_template("fanno.html", gamma=gamma)

# Defining the rayleigh flow page
@app.route("/rayleigh")
def rayleigh():
    return render_template("rayleigh.html")

# Defining the isentropic flow page
@app.route("/isentropic", methods=["POST", "GET"])
def isentropic():
    if request.method == "POST":
        fluid = request.form["fluid"]
        gamma = request.form["gamma"]
        M = request.form["M"]
        P = request.form["P"]
        P0 = request.form["P0"]
        Pstar = request.form["Pstar"]
        P0_P = request.form["P0_P"]
        P0_Pstar = request.form["P0_Pstar"]
        T = request.form["T"]
        T0 = request.form["T0"]
        Tstar = request.form["Tstar"]
        T0_T = request.form["T0_T"]
        T0_Tstar = request.form["T0_Tstar"]
        rho = request.form["rho"]
        rho0 = request.form["rho0"]
        rhostar = request.form["rhostar"]
        rho0_rho = request.form["rho0_rho"]
        rho0_rhostar = request.form["rho0_rhostar"]
        A = request.form["A"]
        Astar = request.form["Astar"]
        A_Astar = request.form["A_Astar"]
        a0_a = request.form["a0_a"]
        regime = request.form["regime"]

        gamma = float(gamma) if gamma else None
        M = float(M) if M else None
        P = float(P) if P else None
        P0 = float(P0) if P0 else None
        Pstar = float(Pstar) if Pstar else None
        P0_P = float(P0_P) if P0_P else None
        P0_Pstar = float(P0_Pstar) if P0_Pstar else None
        T = float(T) if T else None
        T0 = float(T0) if T0 else None
        Tstar = float(Tstar) if Tstar else None
        T0_T = float(T0_T) if T0_T else None
        T0_Tstar = float(T0_Tstar) if T0_Tstar else None
        rho = float(rho) if rho else None
        rho0 = float(rho0) if rho0 else None
        rhostar = float(rhostar) if rhostar else None
        rho0_rho = float(rho0_rho) if rho0_rho else None
        rho0_rhostar = float(rho0_rhostar) if rho0_rhostar else None
        A = float(A) if A else None
        Astar = float(Astar) if Astar else None
        A_Astar = float(A_Astar) if A_Astar else None
        a0_a = float(a0_a) if a0_a else None

        result = isentropicFlow.isentropicFlow(u, fluid=fluid, M=M, P=P, P0=P0, Pstar=Pstar, 
                                                    P0_P=P0_P, P0_Pstar=P0_Pstar, T=T, T0=T0, Tstar=Tstar, 
                                                    T0_T=T0_T, T0_Tstar=T0_Tstar, rho=rho, rho0=rho0, rhostar=rhostar,
                                                    rho0_rho=rho0_rho, rho0_rhostar=rho0_rhostar, A=A, Astar=Astar,
                                                    A_Astar=A_Astar, a0_a=a0_a, gamma=gamma, regime=regime)
        fluid = "" if fluid is None else fluid
        gamma = "" if gamma is None else gamma
        M = "" if result['M'] is None else result['M']
        P = "" if result['P'] is None else result['P']
        P0 = "" if result['P0'] is None else result['P0']
        Pstar = "" if result['Pstar'] is None else result['Pstar']
        P0_P = "" if result['P0_P'] is None else result['P0_P']
        P0_Pstar = "" if result['P0_Pstar'] is None else result['P0_Pstar']
        T = "" if result["T"] is None else result['T']
        T0 = "" if result['T0'] is None else result['T0']
        Tstar = "" if result['Tstar'] is None else result['Tstar']
        T0_T = "" if result['T0_T'] is None else result['T0_T']
        T0_Tstar = "" if result['T0_Tstar'] is None else result['T0_Tstar']
        rho = "" if result['rho'] is None else result['rho']
        rho0 = "" if result['rho0'] is None else result['rho0']
        rhostar = "" if result['rhostar'] is None else result['rhostar']
        rho0_rho = "" if result['rho0_rho'] is None else result['rho0_rho']
        rho0_rhostar = "" if result['rho0_rhostar'] is None else result['rho0_rhostar']
        A = "" if result['A'] is None else result['A']
        Astar = "" if result['Astar'] is None else result['Astar']
        A_Astar = "" if result['A_Astar'] is None else result['A_Astar']
        a0_a = "" if result['a0_a'] is None else result['a0_a']

        return jsonify({
            "fluid": fluid,
            "gamma": gamma,
            "M": M,
            "P": P,
            "P0": P0,
            "Pstar": Pstar,
            "P0_P": P0_P,
            "P0_Pstar": P0_Pstar,
            "T": T,
            "T0": T0,
            "Tstar": Tstar,
            "T0_T": T0_T,
            "T0_Tstar": T0_Tstar,
            "rho": rho,
            "rho0": rho0,
            "rhostar": rhostar,
            "rho0_rho": rho0_rho,
            "rho0_rhostar": rho0_rhostar,
            "A": A,
            "Astar": Astar,
            "A_Astar": A_Astar,
            "a0_a": a0_a
        })
    else:
        gamma = "1.4"

        return render_template("isentropic.html", gamma=gamma)

# Defining the fanno flow page
@app.route("/shocks")
def shocks():
    return render_template("shocks.html")

if __name__ == "__main__":
    app.run(debug=False,host="0.0.0.0", port = 5000) # prod host
    #app.run(debug=True) # dev host
    