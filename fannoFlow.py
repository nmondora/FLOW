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
    from sympy import Symbol
    import standardFlow_TO_massFlow

    # Constants
    R = 8.314 # Ideal Gas Constant

    upstreamTemp = upstreamTemp if upstreamTemp else Q_(68, u.degC)
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
    print(upstreamMach)

    # find downstream mach
    Dh = 4*area / (math.pi * tubeDiam)
    F = (frictionCoeff / Dh.to('meter')) * tubeLen.to('meter')
    upstreamPoint = -1/(gamma*upstreamMach**2) - (gamma+1)/(2*gamma)*math.log(upstreamMach**2 / (1 + (gamma-1)/2 * upstreamMach**2))
    downstreamPoint = F.magnitude + upstreamPoint.magnitude
    x = Symbol('x')
    downstreamPoint = solve(-1/(gamma * x**2) - (gamma+1)/(2*gamma)*math.log(x**2 / (1 + (gamma-1)/2 * x**2)) - (F.magnitude + upstreamPoint.magnitude), x)



    return downstreamPoint