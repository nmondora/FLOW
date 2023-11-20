def standardFlow_TO_massFlow(standardVolFlow, T, P, fluid):
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    #   Inputs:
    #       standardVolFlow: Volumetric flow rate in SCFM (required)
    #       fluid:           Fluid name as string (required)
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    from CoolProp import CoolProp as cp
    from pint import UnitRegistry
    u = UnitRegistry()

    molemass = cp.PropsSI(fluid, 'molemass') * u.kilogram / u.kmol
    R = 8.314 # Ideal Gas Constant

    # STP Conditions
    P = 101325 * u.pascal
    T = 68 * u.degC

    standardVolFlow = standardVolFlow.to('meter^3 / sec')
    massFlow = molemass.to('gram / mol') * P.to('pascal') * standardVolFlow.magnitude / (R * T.to('kelvin')) # kilogram / sec
    return massFlow