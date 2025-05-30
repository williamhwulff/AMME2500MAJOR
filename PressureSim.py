import numpy as np
import matplotlib.pyplot as plt

# Parameters
n_cycles = 10  # number of cycles to plot
deg_per_cycle = 720
total_degrees = n_cycles * deg_per_cycle

# Define angle range
theta = np.arange(1, total_degrees + 1)  # 1 to 2160 degrees
temperature = np.zeros_like(theta, dtype=float) # Kelvins
Volume = np.zeros_like(theta, dtype=float)           
Moles = np.zeros_like(theta, dtype=float)
Pressure = np.zeros_like(theta, dtype=float)

# Loop through each degree
for i in range(len(theta)):
    x = theta[i]
    x_mod = x % deg_per_cycle  # map to one cycle (0–720 degrees)

    # Cosine-based volume function (never zero to avoid div by 0)
    Volume[i] = (225 * np.cos(np.radians(x + 180)) + 275) / 1e6  # Mean 275, oscillates ±225

    # Piecewise function y(x)
    if x_mod < 180:                       # Intake stroke
        Pressure[i] = -30000                          # Fixed pressure for intake stroke
    elif x_mod < 360:                     # Compression stroke
        Pressure[i] = ((30000 * Volume[179]) / Volume[i]) + 30000  
    elif x_mod < 540:                     # Combustion stroke
        x_local = x_mod - 360   #local degrees
        temperature[i] = (2500 * (1 - np.exp(-5 * ((x_local / 80) ** 2)))) + 273 + 60 #Temperature spike
        Moles[i] = (6e-2 * (1 - np.exp(-5 * ((x_local / 80) ** 2)))) + 3.12e-2        # Chemical change mole change
        if Volume[i] != 0:
            Pressure[i] = (Moles[i] * 8.314 * temperature[i]) / Volume[i]
            pEnd = Pressure[i]        # pressure at end of combustion stroke
        else:
            Pressure[i] = 30000
    else:                                # Exhaust stroke       
        slope = (30000 - pEnd) / 180
        Pressure[i] = pEnd + slope * (x_local)

# Plotting
plt.figure(figsize=(12, 6))
plt.plot(theta, Pressure / 1e3, 'r-', linewidth=2, label='Pressure (kPa)')
plt.plot(theta, (Pressure * 4.5e-3), 'k-', linewidth=2, label='Force (N)')
plt.plot(theta, Volume, 'b-', linewidth=2, label='Volume (m^3)')
plt.plot(theta, temperature, 'g-', linewidth=2, label='Temperature (K)')
plt.xlabel('Crank Angle (degrees)')
plt.ylabel('Value')
plt.title('Engine Cycle Function Over Crank Angle')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
