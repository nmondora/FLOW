from pint import UnitRegistry
u = UnitRegistry()
Q_ = u.Quantity
import fannoFlow

ans = fannoFlow.fannoFlow("helium", 1000*u.psi, 1*u.kilogram / u.sec, .25*u.inch, 3*u.foot)