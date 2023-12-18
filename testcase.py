from pint import UnitRegistry
u = UnitRegistry()
Q_ = u.Quantity
import fannoFlow

ans = fannoFlow.fannoFlow("air", 43.5*u.psi, .48*u.kilogram / u.sec, .1*u.meter, 1*u.meter)
print(ans)