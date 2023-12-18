import unittest
from pint import UnitRegistry
u = UnitRegistry()
Q_ = u.Quantity
import fannoFlow
import json

tol = .5 # Values must match withing 0.5%

# calculate % difference between 2 values
def spread(value1, value2):
    # Calculate the percentage difference
    percentage_difference = abs((value1 - value2) / ((value1 + value2) / 2)) * 100
    return percentage_difference

# load test case data
json_file_path = 'fannoTests.json'
with open(json_file_path, 'r') as file:
    # Load the JSON data into a Python dictionary
    data = json.load(file)
cases_list = data.get('cases', [])

# init empty vectors
fluid = []
frictionCoeff = []
constantGamma = []
upstreamPress = []
upstreamTemp = []
upstreamMach = []
upstreamVelocity = []
standardVolFlow = []
massFlow = []
tubeDiameter = []
tubeLength = []
downstreamPressExpected = []
downstreamTempExpected = []
downstreamMachExpected = []

for case in cases_list:
    # Assign values to variables based on the found case
    caseNo = case.get('caseNo') - 1
    fluid[caseNo] = case.get('fluid')
    frictionCoeff[caseNo] = case.get('frictionCoeff')
    constantGamma[caseNo] = case.get('constantGamma')
    upstreamPress[caseNo] = case.get('upstreamPress') * u.pascal
    upstreamTemp[caseNo] = case.get('upstreamTemp')
    upstreamMach[caseNo] = case.get('upstreamMach')
    upstreamVelocity[caseNo] = case.get('upstreamVelocity')
    standardVolFlow[caseNo] = case.get('standardVolFlow')
    massFlow[caseNo] = case.get('massFlow')
    tubeDiameter[caseNo] = case.get('tubeDiameter') * u.meter
    tubeLength[caseNo] = case.get('tubeLength') * u.meter
    downstreamPressExpected[caseNo] = case.get('downstreamPress') * u.pascal
    downstreamTempExpected[caseNo] = case.get('downstreamTemp')
    downstreamMachExpected[caseNo] = case.get('downstreamMach')

    # add units to all optional variables, if passed
    upstreamTemp[caseNo] = Q_(upstreamTemp, u.kelvin) if upstreamTemp is not None else None
    upstreamVelocity[caseNo] = upstreamVelocity *u.meter/u.second if upstreamVelocity is not None else None
    standardVolFlow[caseNo] = standardVolFlow * u.foot**3/u.second if standardVolFlow is not None else None
    massFlow = massFlow[caseNo] * u.kilogram/u.second if massFlow is not None else None
    downstreamTempExpected[caseNo] = Q_(downstreamTempExpected, u.kelvin) if downstreamTempExpected is not None else None

class FannoFlowTests(unittest.TestCase):
    # when adding new tests, copy-past def test_1 and modify value of testno
    def test_1(self):
        testno = 1
        i = testno - 1
        downstreamMach, downstreamPress, downstreamTemp = fannoFlow.fannoFlow(u, fluid=fluid[i], upstreamPress=upstreamPress[i], 
                                                                    tubeDiam=tubeDiameter[i], tubeLen=tubeLength[i],
                                                                    frictionCoeff=frictionCoeff[i], upstreamTemp=upstreamTemp[i],
                                                                    standardVolFlow=standardVolFlow[i], massFlow=massFlow[i],
                                                                    upstreamMach=upstreamMach[i], upstreamVel=upstreamVelocity[i], gamma=constantGamma[i])
        
        downstreamMachSpread = spread(downstreamMach[i], downstreamMachExpected[i])
        downstreamTempSpread = spread(downstreamTemp[i].magnitude, downstreamTempExpected[i].magnitude)
        downstreamPressSpread = spread(downstreamPress[i].magnitude, downstreamPressExpected[i].magnitude)
        self.assertTrue(downstreamMachSpread <= tol, f'Mach spread failed in test_{testno}')
        self.assertTrue(downstreamTempSpread <= tol, f'Temp spread failed in test_{testno}')
        self.assertTrue(downstreamPressSpread <= tol, f'Press spread failed in test_{testno}')

    def test_2(self):
        testno = 2
        i = testno - 1
        downstreamMach, downstreamPress, downstreamTemp = fannoFlow.fannoFlow(u, fluid=fluid[i], upstreamPress=upstreamPress[i], 
                                                                    tubeDiam=tubeDiameter[i], tubeLen=tubeLength[i],
                                                                    frictionCoeff=frictionCoeff[i], upstreamTemp=upstreamTemp[i],
                                                                    standardVolFlow=standardVolFlow[i], massFlow=massFlow[i],
                                                                    upstreamMach=upstreamMach[i], upstreamVel=upstreamVelocity[i], gamma=constantGamma[i])
        
        downstreamMachSpread = spread(downstreamMach[i], downstreamMachExpected[i])
        downstreamTempSpread = spread(downstreamTemp[i].magnitude, downstreamTempExpected[i].magnitude)
        downstreamPressSpread = spread(downstreamPress[i].magnitude, downstreamPressExpected[i].magnitude)
        self.assertTrue(downstreamMachSpread <= tol, f'Mach spread failed in test_{testno}')
        self.assertTrue(downstreamTempSpread <= tol, f'Temp spread failed in test_{testno}')
        self.assertTrue(downstreamPressSpread <= tol, f'Press spread failed in test_{testno}')

    def test_3(self):
        testno = 3
        i = testno - 1
        downstreamMach, downstreamPress, downstreamTemp = fannoFlow.fannoFlow(u, fluid=fluid[i], upstreamPress=upstreamPress[i], 
                                                                    tubeDiam=tubeDiameter[i], tubeLen=tubeLength[i],
                                                                    frictionCoeff=frictionCoeff[i], upstreamTemp=upstreamTemp[i],
                                                                    standardVolFlow=standardVolFlow[i], massFlow=massFlow[i],
                                                                    upstreamMach=upstreamMach[i], upstreamVel=upstreamVelocity[i], gamma=constantGamma[i])
        
        downstreamMachSpread = spread(downstreamMach[i], downstreamMachExpected[i])
        downstreamTempSpread = spread(downstreamTemp[i].magnitude, downstreamTempExpected[i].magnitude)
        downstreamPressSpread = spread(downstreamPress[i].magnitude, downstreamPressExpected[i].magnitude)
        self.assertTrue(downstreamMachSpread <= tol, f'Mach spread failed in test_{testno}')
        self.assertTrue(downstreamTempSpread <= tol, f'Temp spread failed in test_{testno}')
        self.assertTrue(downstreamPressSpread <= tol, f'Press spread failed in test_{testno}')
