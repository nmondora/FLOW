def fannoFlow(fluid, upstreamPress, massFlow, tubeDiam, tubeLen, frictionCoeff=0.58, upstreamTemp=None, standardVolFlow=None):
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # Fanno Flow  -  Flow in relatively short line with constant area, adiabatic frictional
    #   Inputs:
    #       upstreamPress:   Upstream pressure (required)
    #       unstreamTemp:    Upstream temperature (optional, default 68C)
    #       tubeDiam:        Tube inner diameter (required)
    #       tubeLen:         Tube length (required)
    #       frictionCoeff:   Friction coefficient( optional, default )
    #       fluid:           Fluid name as string (required)
    #           massFlow:        Mass flow rate
    #               OR
    #           standardVolFlow: Volumetric flow rate in SCFM
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    from CoolProp import CoolProp as cp
    from pint import UnitRegistry
    u = UnitRegistry()
    Q_ = u.Quantity
    import math
    from sympy.solvers import solve
    from sympy import Symbol, integrate, lambdify
    import standardFlow_TO_massFlow
    from scipy.optimize import fsolve, fminbound, minimize, minimize_scalar, root_scalar
    from scipy.integrate import quad
    import numpy as np

    # Constants
    R = 8.314 # Ideal Gas Constant

    # Standard Temp if none specified
    upstreamTemp = upstreamTemp if upstreamTemp else Q_(68, u.degC)
    # Convert to mass flow rate, if needed
    massFlow = standardFlow_TO_massFlow(standardVolFlow) if standardVolFlow else massFlow

    # XC area
    area = math.pi * (tubeDiam/2)**2

    # find velocity   (continuity)
    upstreamDensity = cp.PropsSI('D', 'T', (upstreamTemp.to('kelvin')).magnitude, 'P', (upstreamPress.to('pascal')).magnitude, fluid) * u.kilogram / (u.meter)**3
    upstreamVel = (massFlow.to('kilogram / sec')).magnitude / ((area.to('meter^2')).magnitude * (upstreamDensity.to('kilogram / meter^3')).magnitude) * u.meter / u.sec

    # find G = density * velocity => constant   (eqn. 13.24a)
    G = massFlow.to('kilogram / sec') / area

    # find upstream mach
    molemass = cp.PropsSI(fluid, 'molemass') * u.kilogram / u.kmol
    Cp = cp.PropsSI('C', 'T', (upstreamTemp.to('kelvin')).magnitude, 'P', (upstreamPress.to('pascal')).magnitude, fluid)
    Cv = cp.PropsSI('O', 'T', (upstreamTemp.to('kelvin')).magnitude, 'P', (upstreamPress.to('pascal')).magnitude, fluid)
    gamma = Cp / Cv
    upstreamC = math.sqrt((gamma * R * upstreamTemp.to('kelvin') / molemass).magnitude) * u.meter / u.sec
    upstreamMach = upstreamVel / upstreamC

    # calculate friction force
    Dh = 4*area / (math.pi * tubeDiam)
    frictionCoeff = .005
    F = frictionCoeff / Dh.to('meter') * tubeLen.to('meter')

    # HARD CODE REMOVE BEFORE MERGE
    upstreamMach = 3
    gamma = 1.4

    # integrated expression for M, see pg.4 of fannoflow_GT.pdf or slide 9 of ReyleighFanno_Anys.pdf
    def func(M, gamma):
        return -1/(gamma * M**2) - (gamma+1)/(2*gamma)*np.log(M**2 / (1 + (gamma-1)/2 * M**2))
    # expression for func(M2)-f(M1)-F=0, see pg.4 of fannoflow_GT.pdf or slide 9 of ReyleighFanno_Anys.pdf
    def fannoFunction(M2, upstreamMach, gamma, F):
        return -1/(gamma * M2**2) - (gamma+1)/(2*gamma)*np.log(M2**2 / (1 + (gamma-1)/2 * M2**2)) - func(upstreamMach,gamma) - F

    # set bounds for downstream mach number based on upstream mach number, see pg. 1 of fannoflow_GT.pdf
    if upstreamMach >= 1:
        boundVec = (1, 10)
    else:
        boundVec = (0, 1)

    # find root of fannoFunction() and determine value of M2, the downstream mach number
    sol = root_scalar(fannoFunction, bracket=boundVec, args=(upstreamMach,gamma,F))
    downstreamMach = sol.root

    return downstreamMach