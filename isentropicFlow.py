def isentropicFlow(u, fluid, M=None, P=None, P0=None, Pstar=None, P0_P=None, P0_Pstar=None, T=None, T0=None, Tstar=None, 
                   T0_T=None, T0_Tstar=None, rho=None, rho0=None, rhostar=None, rho0_rho=None, rho0_rhostar=None, A=None, 
                   Astar=None, A_Astar=None, a0_a=None, gamma=None, regime=None):
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # Isentropic Flow  -  Flow is adiabatic and reversible
    #   Inputs:
    #       u:          Unit registry (pint)
    #       fluid:      Fluid name as string (required)
    #   Outputs:
    #       M2:         Downstream mach number
    #       P2:         Downstream static pressure
    #       T2:         Downstream static temperature
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    from warnings import warn
    from pint import UnitRegistry
    from math import sqrt
    from CoolProp import CoolProp as cp
    from scipy.optimize import fsolve
    #u = UnitRegistry()
    Q_ = u.Quantity

    # add base units if none are passed
    P = P if P is None or isinstance(P, Q_) else P * u.pascal
    P0 = P0 if P0 is None or isinstance(P0, Q_) else P0 * u.pascal
    Pstar = Pstar if Pstar is None or isinstance(Pstar, Q_) else Pstar * u.pascal
    T = T if T is None or isinstance(T, Q_) else Q_(T, u.kelvin)
    T0 = T0 if T0 is None or isinstance(T0, Q_) else Q_(T0, u.kelvin)
    Tstar = Tstar if Tstar is None or isinstance(Tstar, Q_) else Q_(Tstar, u.kelvin)
    rho = rho if rho is None or isinstance(rho, Q_) else rho * u.kilogram/u.meter**3
    rho0 = rho0 if rho0 is None or isinstance(rho0, Q_) else rho0 * u.kilogram/u.meter**3
    rhostar = rhostar if rhostar is None or isinstance(rhostar, Q_) else rhostar * u.kilogram/u.meter**3
    A = A if A is None or isinstance(A, Q_) else A * u.meter**2
    Astar = Astar if Astar is None or isinstance(Astar, Q_) else Astar * u.meter**2

    # find specific heats of fluid at upstream conditions
    if gamma is None:
        Cp = cp.PropsSI('C', 'T', T.magnitude, 'P', P.magnitude, fluid)
        Cv = cp.PropsSI('O', 'T', T.magnitude, 'P', P.magnitude, fluid)
        gamma = Cp / Cv
    gm1 = gamma - 1
    gp1 = gamma + 1

    def criticalConditions(gamma, M):
        gp1 = gamma + 1
        gm1 = gamma - 1

        P0_Pstar = (.5 * gp1)**(gamma/gm1)
        T0_Tstar = gp1 / 2
        rho0_rhostar = (.5 * gp1)**(1/gm1)
        A_Astar = (1/M) * sqrt(((1+.5*gm1*M**2) / (1+.5*gm1))**(gp1/gm1))

        return P0_Pstar, T0_Tstar, rho0_rhostar, A_Astar
    
    def isentropicRelation(gamma, M):
        gp1 = gamma + 1
        gm1 = gamma - 1

        P0_P = (1 + .5*gm1*M**2)**(gamma/gm1)
        T0_T = 1 + .5*gm1*M**2
        rho0_rho = (1 + .5*gm1*M**2)**(1/gm1)
        a0_a = (1 + .5*gm1*M**2)**(.5)

        return P0_P, T0_T, rho0_rho, a0_a

    if M is not None:
        # check if there might be conflicting inputs
        if A_Astar is not None or T0_T is not None or T0_Tstar is not None or P0_P is not None or P0_Pstar is not None or rho0_rho is not None or rho0_rhostar is not None or a0_a is not None:
            warn('Too many inputs may be given. Solving using M')

        # calculate ratio terms using M
        P0_Pstar, T0_Tstar, rho0_rhostar, A_Astar = criticalConditions(gamma, M)
        P0_P, T0_T, rho0_rho, a0_a = isentropicRelation(gamma, M)

        # calculare pressure terms based on what is / isn't known
        P0 = P0_P * P if P is not None and P0 is None else P0_Pstar * Pstar if Pstar is not None and P0 is None else P0
        P = 1/P0_P * P0 if P0 is not None and P is None else P
        Pstar = 1/P0_Pstar * P0 if P0 is not None and Pstar is None else Pstar

        # calculate temp terms based on what is / isn't known
        T0 = T0_T * T if T is not None and T0 is None else T0_Tstar * Tstar if Tstar is not None and T0 is None else T0
        T = 1/T0_T * T0 if T0 is not None and T is None else T
        Tstar = 1/T0_Tstar * T0 if T0 is not None and Tstar is None else Tstar

        # calculate density terms based on what is / isn't known
        rho0 = rho0_rho * rho if rho is not None and rho0 is None else rho0_rhostar * rhostar if rhostar is not None and rho0 is None else rho0
        rho = 1/rho0_rho * rho0 if rho0 is not None and rho is None else rho
        rhostar = 1/rho0_rhostar * rho0 if rho0 is not None and rhostar is None else rhostar

        # calculate area terms based on what is / isn't known
        A = A_Astar * Astar if Astar is not None and A is None else A
        Astar = 1/A_Astar * A if A is not None and Astar is None else Astar
    elif A_Astar is not None:
        # check if there might be conflicting inputs
        if T0_T is not None or T0_Tstar is not None or P0_P is not None or P0_Pstar is not None or rho0_rho is not None or rho0_rhostar is not None or a0_a is not None:
            warn('Too many inputs may be given. Solving using A/A*') 
        
        func = lambda M: (1/M)*(2/gp1 * (1+.5*gm1*M**2))**(gp1/(2*gm1)) - A_Astar
        guess = 5 if regime == 'supersonic' or regime == 'sup' or regime == 'super' else 0.5
        M = fsolve(func, guess)

        # calculate ratio terms using M
        P0_Pstar, T0_Tstar, rho0_rhostar, A_Astar = criticalConditions(gamma, M)
        P0_P, T0_T, rho0_rho, a0_a = isentropicRelation(gamma, M)

        # calculare pressure terms based on what is / isn't known
        P0 = P0_P * P if P is not None and P0 is None else P0_Pstar * Pstar if Pstar is not None and P0 is None else P0
        P = 1/P0_P * P0 if P0 is not None and P is None else P
        Pstar = 1/P0_Pstar * P0 if P0 is not None and Pstar is None else Pstar

        # calculate temp terms based on what is / isn't known
        T0 = T0_T * T if T is not None and T0 is None else T0_Tstar * Tstar if Tstar is not None and T0 is None else T0
        T = 1/T0_T * T0 if T0 is not None and T is None else T
        Tstar = 1/T0_Tstar * T0 if T0 is not None and Tstar is None else Tstar

        # calculate density terms based on what is / isn't known
        rho0 = rho0_rho * rho if rho is not None and rho0 is None else rho0_rhostar * rhostar if rhostar is not None and rho0 is None else rho0
        rho = 1/rho0_rho * rho0 if rho0 is not None and rho is None else rho
        rhostar = 1/rho0_rhostar * rho0 if rho0 is not None and rhostar is None else rhostar

        # calculate area terms based on what is / isn't known
        A = A_Astar * Astar if Astar is not None and A is None else A

    result = {
        'M': M, 'P': P, 'P0': P0, 'Pstar': Pstar, 'P0_P': P0_P, 'P0_Pstar': P0_Pstar, 'T': T, 'T0': T0,
        'Tstar': Tstar, 'T0_T': T0_T, 'T0_Tstar': T0_Tstar,'rho': rho, 'rho0': rho0, 'rhostar': rhostar,
        'rho0_rho': rho0_rho, 'rho0_rhostar': rho0_rhostar, 'A': A, 'Astar': Astar, 'A_Astar': A_Astar, 'a0_a': a0_a
    }

    return result
    

