import unittest
from pint import UnitRegistry
u = UnitRegistry()
Q_ = u.Quantity
from isentropicFlow import isentropicFlow
import json

tol = .5 # Values must match withing 0.5%

# calculate % difference between 2 values
def spread(value1, value2):
    # Calculate the percentage difference
    percentage_difference = abs((value1 - value2) / ((value1 + value2) / 2)) * 100
    return percentage_difference

# load test case data
json_file_path = 'isentropicUnitTests.json'
with open(json_file_path, 'r') as file:
    # Load the JSON data into a Python dictionary
    data = json.load(file)
cases_list = data.get('cases', [])
length = len(cases_list)

# init empty vectors
fluid = [None] * length
M_IN = [None] * length
M_OUT = [None] * length
P_IN = [None] * length
P_OUT = [None] * length
P0_IN = [None] * length
P0_OUT = [None] * length
Pstar_IN = [None] * length
Pstar_OUT = [None] * length
T_IN = [None] * length
T_OUT = [None] * length
T0_IN = [None] * length
T0_OUT = [None] * length
Tstar_IN = [None] * length
Tstar_OUT = [None] * length
rho_IN = [None] * length
rho_OUT = [None] * length
rho0_IN = [None] * length
rho0_OUT = [None] * length
rhostar_IN = [None] * length
rhostar_OUT = [None] * length
A_IN = [None] * length
A_OUT = [None] * length
Astar_IN = [None] * length
Astar_OUT = [None] * length
gamma_IN = [None] * length
gamma_OUT = [None] * length
P0_P_IN = [None] * length
P0_P_OUT = [None] * length
P0_Pstar_IN = [None] * length
P0_Pstar_OUT = [None] * length
T0_T_IN = [None] * length
T0_T_OUT = [None] * length
T0_Tstar_IN = [None] * length
T0_Tstar_OUT = [None] * length
rho0_rho_IN = [None] * length
rho0_rho_OUT = [None] * length
rho0_rhostar_IN = [None] * length
rho0_rhostar_OUT = [None] * length
A_Astar_IN = [None] * length
A_Astar_OUT = [None] * length

for case in cases_list:
    # Assign values to variables based on the found case
    caseNo = case.get('caseNo') - 1
    inputs = case.get('inputs', [])
    outputs = case.get('outputs', [])

    fluid[caseNo] = case.get('fluid')

    M_IN[caseNo] = inputs.get('M')
    M_OUT[caseNo] = outputs.get('M')
    P_IN[caseNo] = inputs.get('P') * u.pascal if inputs.get('P') is not None else None
    P_OUT[caseNo] = outputs.get('P') * u.pascal if outputs.get('P') is not None else None
    P0_IN[caseNo] = inputs.get('P0') * u.pascal if inputs.get('P0') is not None else None
    P0_OUT[caseNo] = outputs.get('P0') * u.pascal if outputs.get('P0') is not None else None
    Pstar_IN[caseNo] = inputs.get('Pstar') * u.pascal if inputs.get('Pstar') is not None else None
    Pstar_OUT[caseNo] = outputs.get('Pstar') * u.pascal if outputs.get('Pstar') is not None else None
    T_IN[caseNo] = Q_(inputs.get('T'), u.kelvin) if inputs.get('T') is not None else None
    T_OUT[caseNo] = Q_(outputs.get('T'), u.kelvin) if outputs.get('T') is not None else None
    T0_IN[caseNo] = Q_(inputs.get('T0'), u.kelvin) if inputs.get('T0') is not None else None
    T0_OUT[caseNo] = Q_(outputs.get('T0'), u.kelvin) if outputs.get('T0') is not None else None
    Tstar_IN[caseNo] = Q_(inputs.get('Tstar'), u.kelvin) if inputs.get('Tstar') is not None else None
    Tstar_OUT[caseNo] = Q_(outputs.get('Tstar'), u.kelvin) if outputs.get('Tstar') is not None else None
    rho_IN[caseNo] = inputs.get('rho') * u.kilogram/u.meter**3 if inputs.get('rho') is not None else None
    rho_OUT[caseNo] = outputs.get('rho') * u.kilogram/u.meter**3 if outputs.get('rho') is not None else None
    rho0_IN[caseNo] = inputs.get('rho0') * u.kilogram/u.meter**3 if inputs.get('rho0') is not None else None
    rho0_OUT[caseNo] = outputs.get('rho0') * u.kilogram/u.meter**3 if outputs.get('rho0') is not None else None
    rhostar_IN[caseNo] = inputs.get('rhostar') * u.kilogram/u.meter**3 if inputs.get('rhostar') is not None else None
    rhostar_OUT[caseNo] = outputs.get('rhostar') * u.kilogram/u.meter**3 if outputs.get('rhostar') is not None else None
    A_IN[caseNo] = inputs.get('A') * u.meter**2 if inputs.get('A') is not None else None
    A_OUT[caseNo] = outputs.get('A') * u.meter**2 if outputs.get('A') is not None else None
    Astar_IN[caseNo] = inputs.get('Astar') * u.meter**2 if inputs.get('Astar') is not None else None
    Astar_OUT[caseNo] = outputs.get('Astar') * u.meter**2 if outputs.get('Astar') is not None else None
    gamma_IN[caseNo] = inputs.get('gamma')
    gamma_OUT[caseNo] = outputs.get('gamma')
    P0_P_IN[caseNo] = inputs.get('P0_P')
    P0_P_OUT[caseNo] = outputs.get('P0_P')
    P0_Pstar_IN[caseNo] = inputs.get('P0_Pstar')
    P0_Pstar_OUT[caseNo] = outputs.get('P0_Pstar')
    T0_T_IN[caseNo] = inputs.get('T0_T')
    T0_T_OUT[caseNo] = outputs.get('T0_T')
    T0_Tstar_IN[caseNo] = inputs.get('T0_Tstar')
    T0_Tstar_OUT[caseNo] = outputs.get('T0_Tstar')
    rho0_rho_IN[caseNo] = inputs.get('rho0_rho')
    rho0_rho_OUT[caseNo] = outputs.get('rho0_rho')
    rho0_rhostar_IN[caseNo] = inputs.get('rho0_rhostar')
    rho0_rhostar_OUT[caseNo] = outputs.get('rho0_rhostar')
    A_Astar_IN[caseNo] = inputs.get('A_Astar')
    A_Astar_OUT[caseNo] = outputs.get('A_Astar')
    
class IsentropicFlowTests(unittest.TestCase):
    # when adding new tests, copy-past def test_1 and modify value of testno
    def test_1(self):
        testno = 1
        i = testno - 1

        out = isentropicFlow(u, fluid[i], M=M_IN[i], P=P_IN[i], P0=P0_IN[i], Pstar=Pstar_IN[i], 
                                                                                     T=T_IN[i], T0=T0_IN[i], Tstar=Tstar_IN[i], rho=rho0_IN[i], rho0=rho0_IN[i], rhostar=rhostar_IN[i], A=A_IN[i], Astar=Astar_IN[i], 
                                                                                     gamma=gamma_IN[i])
        self.assertTrue(M_OUT[i] is None or spread(out.get('M'), M_OUT[i]) <= tol, f'M spread failed in test_{testno}')
        self.assertTrue(P_OUT[i] is None or spread(out.get('P'), P_OUT[i]) <= tol, f'P spread failed in test_{testno}')
        self.assertTrue(P0_OUT[i] is None or spread(out.get('P0'), P0_OUT[i]) <= tol, f'P0 spread failed in test_{testno}')
        self.assertTrue(Pstar_OUT[i] is None or spread(out.get('Pstar'), Pstar_OUT[i]) <= tol, f'Pstar spread failed in test_{testno}')
        self.assertTrue(T_OUT[i] is None or spread(out.get('T'), T_OUT[i]) <= tol, f'T spread failed in test_{testno}')
        self.assertTrue(T0_OUT[i] is None or spread(out.get('T0'), T0_OUT[i]) <= tol, f'T0 spread failed in test_{testno}')
        self.assertTrue(Tstar_OUT[i] is None or spread(out.get('Tstar'), Tstar_OUT[i]) <= tol, f'Tstar spread failed in test_{testno}')
        self.assertTrue(rho_OUT[i] is None or spread(out.get('rho'), rho_OUT[i]) <= tol, f'rho spread failed in test_{testno}')
        self.assertTrue(rho0_OUT[i] is None or spread(out.get('rho0'), rho0_OUT[i]) <= tol, f'rho0 spread failed in test_{testno}')
        self.assertTrue(rhostar_OUT[i] is None or spread(out.get('rhostar'), rhostar_OUT[i]) <= tol, f'rhostar spread failed in test_{testno}')
        self.assertTrue(A_OUT[i] is None or spread(out.get('A'), A_OUT[i]) <= tol, f'A spread failed in test_{testno}')
        self.assertTrue(Astar_OUT[i] is None or spread(out.get('Astar'), Astar_OUT[i]) <= tol, f'Astar spread failed in test_{testno}')

if __name__ == '__main__':
    unittest.main()