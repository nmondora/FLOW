import unittest
from pint import UnitRegistry
u = UnitRegistry()
Q_ = u.Quantity
import isentropicFlow
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
        M_out, P_out, P0_out, Pstar_out, T_out, T0_out, Tstar_out, rho_out, rho0_out, rhostar_out, A_out, Astar_out = isentropicFlow(u, fluid, M=None, P=None, P0=None, Pstar=None, 
                                                                                     T=None, T0=None, Tstar=None, rho=None, rho0=None, rhostar=None, A=None, Astar=None, gamma=None)
        self.assertTrue(spread(M_out, M_OUT) <= tol, f'M spread failed in test_{testno}') if M_OUT is not None else None
        self.assertTrue(spread(P_out, P_OUT) <= tol, f'P spread failed in test_{testno}') if P_OUT is not None else None
        self.assertTrue(spread(P0_out, P0_OUT) <= tol, f'P0 spread failed in test_{testno}') if P0_OUT is not None else None
        self.assertTrue(spread(Pstar_out, Pstar_OUT) <= tol, f'Pstar spread failed in test_{testno}') if Pstar_OUT is not None else None
        self.assertTrue(spread(T_out, T_OUT) <= tol, f'T spread failed in test_{testno}') if T_OUT is not None else None
        self.assertTrue(spread(T0_out, T0_OUT) <= tol, f'T0 spread failed in test_{testno}') if T0_OUT is not None else None
        self.assertTrue(spread(Tstar_out, Tstar_OUT) <= tol, f'Tstar spread failed in test_{testno}') if Tstar_OUT is not None else None
        self.assertTrue(spread(rho_out, rho_OUT) <= tol, f'rho spread failed in test_{testno}') if rho_OUT is not None else None
        self.assertTrue(spread(rho0_out, rho0_OUT) <= tol, f'rho0 spread failed in test_{testno}') if rho0_OUT is not None else None
        self.assertTrue(spread(rhostar_out, rhostar_OUT) <= tol, f'rhostar spread failed in test_{testno}') if rhostar_OUT is not None else None
        self.assertTrue(spread(A_out, A_OUT) <= tol, f'A spread failed in test_{testno}') if A_OUT is not None else None
        self.assertTrue(spread(Astar_out, Astar_OUT) <= tol, f'Astar spread failed in test_{testno}') if Astar_OUT is not None else None


if __name__ == '__main__':
    unittest.main()