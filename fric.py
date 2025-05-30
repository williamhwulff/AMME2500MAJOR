import math
def viscous_friction_crank(N):
    eta = 0.25     # Pa·s (motor oil) 
    L = 0.08       # Length of crank
    R = 0.02       # Radius of crank 
    d = 0.030      # thickness of oil film (m)
    # Calculate viscous torque
    torque = (4 * math.pi**2 * eta * L * R**3 * N) / d
    # Calculate viscous force
    force = torque / R
    return force

def viscous_friction_piston(v):
    eta = 0.25      # Pa·s
    D = 0.0757      # 75.7 mm
    h = 0.04        # 40 mm
    d = 0.00002     # 20 microns
    A = math.pi * D * h  # side surface area of piston
    F = eta * A * v / d
    return F
w = 10          # m/s, just integral of position
N = 50          # rotational speed !!!m/s  [RPM/60]
F_crank = viscous_friction_piston(w)
F_piston = viscous_friction_crank(N)
print(f"Crank Friction Force: {F_crank:.2f} N")
print(f"Piston Friction Force:  {F_piston:.2f} N")