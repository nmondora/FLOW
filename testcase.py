from pint import UnitRegistry
u = UnitRegistry()
Q_ = u.Quantity
import fannoFlow
import json

tol = .5 # Values must match withing 0.5%

class TextColors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    END = '\033[0m'

# calculate % difference between 2 values
def spread(value1, value2, tol):
    # Calculate the percentage difference
    percentage_difference = abs((value1 - value2) / ((value1 + value2) / 2)) * 100
    textColor = '\033[92m' if percentage_difference < tol else '\033[91m'
    return percentage_difference, textColor

# load test case data
json_file_path = 'fannoTests.json'
with open(json_file_path, 'r') as file:
    # Load the JSON data into a Python dictionary
    data = json.load(file)
cases_list = data.get('cases', [])

for case in cases_list:
    # Assign values to variables based on the found case
    caseNo = case.get('caseNo')
    fluid = case.get('fluid')
    frictionCoeff = case.get('frictionCoeff')
    constantGamma = case.get('constantGamma')
    upstreamPress = case.get('upstreamPress') * u.pascal
    upstreamTemp = case.get('upstreamTemp')
    upstreamMach = case.get('upstreamMach')
    upstreamVelocity = case.get('upstreamVelocity')
    standardVolFlow = case.get('standardVolFlow')
    massFlow = case.get('massFlow')
    tubeDiameter = case.get('tubeDiameter') * u.meter
    tubeLength = case.get('tubeLength') * u.meter
    downstreamPressExpected = case.get('downstreamPress') * u.pascal
    downstreamTempExpected = case.get('downstreamTemp')
    downstreamMachExpected = case.get('downstreamMach')

    # add units to all optional variables, if passed
    upstreamTemp = Q_(upstreamTemp, u.kelvin) if upstreamTemp is not None else None
    upstreamVelocity = upstreamVelocity *u.meter/u.second if upstreamVelocity is not None else None
    standardVolFlow = standardVolFlow * u.foot**3/u.second if standardVolFlow is not None else None
    massFlow = massFlow * u.kilogram/u.second if massFlow is not None else None
    downstreamTempExpected = Q_(downstreamTempExpected, u.kelvin) if downstreamTempExpected is not None else None

    gamma = [None, constantGamma]
    msg = ["Using CoolProp value for gamma", "Using passed value for gamma"]

    for i in range(2):
        # run fannoFlow() and assign outputs
        downstreamMach, downstreamPress, downstreamTemp = fannoFlow.fannoFlow(u, fluid=fluid, upstreamPress=upstreamPress, 
                                                                            tubeDiam=tubeDiameter, tubeLen=tubeLength,
                                                                            frictionCoeff=frictionCoeff, upstreamTemp=upstreamTemp,
                                                                            standardVolFlow=standardVolFlow, massFlow=massFlow,
                                                                            upstreamMach=upstreamMach, upstreamVel=upstreamVelocity, gamma=gamma[i])

        # check if outputs match expected values
        print(TextColors.MAGENTA + f'Test Case: {caseNo}' + TextColors.END)
        downstreamMachSpread, textColor = spread(downstreamMach, downstreamMachExpected, tol)
        print(f'{textColor}\tDownstream Mach:  {downstreamMachSpread:.2f}% ({downstreamMach:0.3f} vs. {downstreamMachExpected:0.3f})\033[0m')
        downstreamTempSpread, textColor = spread(downstreamTemp.magnitude, downstreamTempExpected.magnitude, tol)
        print(f'{textColor}\tDownstream Temp:  {downstreamTempSpread:.2f}% ({downstreamTemp:0.3f} vs. {downstreamTempExpected:0.3f})\033[0m')
        downstreamPressSpread, textColor = spread(downstreamPress.magnitude, downstreamPressExpected.magnitude, tol)
        print(f'{textColor}\tDownstream Press: {downstreamPressSpread:.2f}% ({downstreamPress:0.3f} vs. {downstreamPressExpected:0.3f})\033[0m\n')

