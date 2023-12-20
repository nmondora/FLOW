def fannoFlow(u, fluid, upstreamPress, tubeDiam, tubeLen, frictionCoeff=0.58, upstreamTemp=None, 
              standardVolFlow=None, massFlow=None, upstreamMach=None, upstreamVel=None, gamma=None):
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # Fanno Flow  -  Flow in relatively short line with constant area, adiabatic frictional
    #   Inputs:
    #       u:                Unit registry (pint)
    #       upstreamPress:    Upstream pressure (required)
    #       unstreamTemp:     Upstream temperature (optional, default 68C)
    #       tubeDiam:         Tube inner diameter (required)
    #       tubeLen:          Tube length (required)
    #       frictionCoeff:    Friction coefficient( optional, default )
    #       fluid:            Fluid name as string (required)
    #        massFlow:        Mass flow rate
    #          OR
    #        standardVolFlow: Volumetric flow rate in SCFM
    #          OR
    #        upstreamMach:    Upstream mach number
    #          OR
    #        upstreamVel:     Upstream flow velocity
    #   Outputs:
    #       downstreamMach:   Downstream mach number
    #       downstreamPress:  Downstream static pressure
    #       downstreamTemp:   Downstream static temperature
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    from CoolProp import CoolProp as cp
    from pint import UnitRegistry
    #u = UnitRegistry()
    Q_ = u.Quantity
    import math
    from ..calculators import standardFlow_TO_massFlow
    from scipy.optimize import root_scalar
    import numpy as np

    # make sure we have everything we need
    if standardVolFlow is None and massFlow is None and upstreamMach is None and upstreamVel is None:
        raise("Not enought info! Provide a flow rate OR upstream mach number OR velocity.")

    # Constants
    R = 8.314 # Ideal Gas Constant

    # Standard Temp if none specified
    upstreamTemp = upstreamTemp if upstreamTemp is not None else Q_(293.15, u.kelvin)

    # Assert pressure in Pascal
    upstreamPress = upstreamPress.to('pascal')

    # XC area
    area = math.pi * (tubeDiam/2)**2

    # find specific heats of fluid at upstream conditions
    Cp = cp.PropsSI('C', 'T', upstreamTemp.magnitude, 'P', upstreamPress.magnitude, fluid)
    Cv = cp.PropsSI('O', 'T', upstreamTemp.magnitude, 'P', upstreamPress.magnitude, fluid)
    gamma = Cp / Cv if gamma is None else gamma

    # if M1 is not known, find it
    if upstreamMach is None:
        # Convert to mass flow rate, if needed
        massFlow = standardFlow_TO_massFlow.standardFlow_TO_massFlow(standardVolFlow) if standardVolFlow else massFlow

        if upstreamVel is None:
            # find velocity   (continuity)
            upstreamDensity = cp.PropsSI('D', 'T', upstreamTemp.magnitude, 'P', upstreamPress.magnitude, fluid) * u.kilogram / (u.meter)**3
            upstreamVel = (massFlow.to('kilogram / sec')).magnitude / ((area.to('meter^2')).magnitude * (upstreamDensity.to('kilogram / meter^3')).magnitude) * u.meter / u.sec
        else:
            upstreamVel = upstreamVel.to('meter / sec')

        # find upstream mach
        molemass = cp.PropsSI(fluid, 'molemass') * u.kilogram / u.kmol
        upstreamC = math.sqrt((gamma * R * upstreamTemp.magnitude / molemass.magnitude)) * u.meter / u.sec
        upstreamMach = upstreamVel / upstreamC

    # calculate friction force
    F = frictionCoeff / tubeDiam.to('meter') * tubeLen.to('meter')

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
        boundVec = (0.01, 1)

    # find root of fannoFunction() and determine value of M2, the downstream mach number
    sol = root_scalar(fannoFunction, bracket=boundVec, args=(upstreamMach,gamma,F))
    downstreamMach = sol.root

    # calculate downstream static temp, see pg. 6/7 of fannoflow_GT.pdf
    downstreamTemp = upstreamTemp.to('kelvin') * (1+(gamma-1)*.5*upstreamMach**2) / (1+(gamma-1)*.5*downstreamMach**2)

    # calculate downstream static pressure, see pg. 6/8 of fannoflow_GT.pdf
    downstreamPress = upstreamPress.to('pascal')*(upstreamMach/downstreamMach)*math.sqrt(downstreamTemp/upstreamTemp)

    return downstreamMach, downstreamPress, downstreamTemp