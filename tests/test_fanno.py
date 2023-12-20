import unittest
from pint import UnitRegistry
u = UnitRegistry()
Q_ = u.Quantity
from ..calculators import fannoFlow
import json

tol = .5 # Values must match withing 0.5%

# calculate % difference between 2 values
def spread(value1, value2):
    # Calculate the percentage difference
    percentage_difference = abs((value1 - value2) / ((value1 + value2) / 2)) * 100
    return percentage_difference

# load test case data
json_file_path = './tests/fannoUnitTests.json'
with open(json_file_path, 'r') as file:
    # Load the JSON data into a Python dictionary
    data = json.load(file)
cases_list = data.get('cases', [])
length = len(cases_list)

# init empty vectors
fluid = [None] * length
frictionCoeff = [None] * length
constantGamma = [None] * length
upstreamPress = [None] * length
upstreamTemp = [None] * length
upstreamMach = [None] * length
upstreamVelocity = [None] * length
standardVolFlow = [None] * length
massFlow = [None] * length
tubeDiameter = [None] * length
tubeLength = [None] * length
downstreamPressExpected = [None] * length
downstreamTempExpected = [None] * length
downstreamMachExpected = [None] * length

for case in cases_list:
    # Assign values to variables based on the found case
    caseNo = case.get('caseNo') - 1
    fluid[caseNo] = case.get('fluid')
    frictionCoeff[caseNo] = case.get('frictionCoeff')
    constantGamma[caseNo] = case.get('constantGamma')
    upstreamPress[caseNo] = case.get('upstreamPress') * u.pascal if case.get('upstreamPress') is not None else None
    upstreamTemp[caseNo] = case.get('upstreamTemp')
    upstreamMach[caseNo] = case.get('upstreamMach')
    upstreamVelocity[caseNo] = case.get('upstreamVelocity')
    standardVolFlow[caseNo] = case.get('standardVolFlow')
    massFlow[caseNo] = case.get('massFlow')
    tubeDiameter[caseNo] = case.get('tubeDiameter') * u.meter if case.get('tubeDiameter') is not None else None
    tubeLength[caseNo] = case.get('tubeLength') * u.meter if case.get('tubeLength') is not None else None
    downstreamPressExpected[caseNo] = case.get('downstreamPress') * u.pascal if case.get('downstreamPress') is not None else None
    downstreamTempExpected[caseNo] = case.get('downstreamTemp')
    downstreamMachExpected[caseNo] = case.get('downstreamMach')

    # add units to all optional variables, if passed
    upstreamTemp[caseNo] = Q_(upstreamTemp[caseNo], u.kelvin) if upstreamTemp[caseNo] is not None else None
    upstreamVelocity[caseNo] = upstreamVelocity[caseNo] *u.meter/u.second if upstreamVelocity[caseNo] is not None else None
    standardVolFlow[caseNo] = standardVolFlow[caseNo] * u.foot**3/u.second if standardVolFlow[caseNo] is not None else None
    massFlow[caseNo] = massFlow[caseNo] * u.kilogram/u.second if massFlow[caseNo] is not None else None
    downstreamTempExpected[caseNo] = Q_(downstreamTempExpected[caseNo], u.kelvin) if downstreamTempExpected[caseNo] is not None else None

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
        
        downstreamMachSpread = spread(downstreamMach, downstreamMachExpected[i])
        downstreamTempSpread = spread(downstreamTemp.magnitude, downstreamTempExpected[i].magnitude)
        downstreamPressSpread = spread(downstreamPress.magnitude, downstreamPressExpected[i].magnitude)
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
        
        downstreamMachSpread = spread(downstreamMach, downstreamMachExpected[i])
        downstreamTempSpread = spread(downstreamTemp.magnitude, downstreamTempExpected[i].magnitude)
        downstreamPressSpread = spread(downstreamPress.magnitude, downstreamPressExpected[i].magnitude)
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
        
        downstreamMachSpread = spread(downstreamMach, downstreamMachExpected[i])
        downstreamTempSpread = spread(downstreamTemp.magnitude, downstreamTempExpected[i].magnitude)
        downstreamPressSpread = spread(downstreamPress.magnitude, downstreamPressExpected[i].magnitude)
        self.assertTrue(downstreamMachSpread <= tol, f'Mach spread failed in test_{testno}')
        self.assertTrue(downstreamTempSpread <= tol, f'Temp spread failed in test_{testno}')
        self.assertTrue(downstreamPressSpread <= tol, f'Press spread failed in test_{testno}')

if __name__ == '__main__':
    unittest.main()