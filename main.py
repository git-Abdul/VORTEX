import math
import sqlite3
import numpy as np
import matplotlib.pyplot as plt

"""
~ Assumptions: 
   [1] Beam provides 1000 electrons/sec (Ro)
   [2] Energy of the beam ≃ 1GeV (Eo)
   [3] Radius of the beam = 2cm (r)
   [4] Assuming a peak width of 0.5 keV for optimal visualization.
"""

cursor = sqlite3.connect('elements.db').cursor()

def convert_unit(value: float, type: str):
    if type == "frequency":
        return value*math.pow(10,15) # In Hertz
    elif type == "energy":
        return value*1000*1.602*math.pow(10,-19) # In joules

element_name = input("Enter the name of the element: ").lower().capitalize()
cursor.execute(f"SELECT energy, f_yield, atomic_number, k_value FROM elements WHERE name = ?", (element_name,))
value = cursor.fetchall()

# Data values
energy = value[0][0]
omega = value[0][1] # Yield
atomic_number = value[0][2]
frequency = energy*1000*1.602/6.626 # Frequency in PHz
power = 1.602*math.pow(10,-6) # Power of the beam: Rate of electrons*(Energy of 1 electron at 1GeV)
area = 0.02*0.02*np.pi
intensity = omega*power/area
amplitude = math.sqrt(2*intensity/(3*8.85*math.pow(10,-4)))

period = 1 / frequency
x = np.linspace(0, 4 * period, 1000) 
y = amplitude * np.sin(2 * np.pi * frequency * x)

plt.figure(figsize=(10, 5))
plt.plot(x, y, label=f"Energy: {energy} keV", color='tab:blue')

if frequency > 10:
    plt.xlim(0, period * 4)
else:
    plt.xlim(0, period * 4)

plt.ylim(-amplitude * 1.2, amplitude * 1.2)

plt.xlabel("Time (fsec)")
plt.ylabel("Amplitude (V/m)")
plt.title(f"X-ray Waveform Generated using {element_name}")

plt.grid(True, which='both', linestyle='--', alpha=0.6)
plt.axhline(y=0, color='k', linewidth=1)
plt.legend(loc="upper right")

plt.show()

def b_curve():
    k=value[0][3] #Empirical attenuation constant (k)
    x = np.linspace(0.1,150,1000)
    y_curve = (150 - x)*np.exp(-k/x**3) # I = Z*(Emax-E)*e^-k/E^3
    y_peak = 100*omega*np.exp(-(x - energy)**2/(2 * 0.5**2))
    y = y_curve+y_peak

    plt.plot(x, y)

    plt.xlabel("Photon energy (keV)")
    plt.ylabel("Intensity")
    plt.title(f"Bremsstrahlung curve of {element_name} (Kα)")

    plt.grid(True, which='both')
    plt.axhline(y=0, color='k')

    plt.show()

choice = input("Show graph for bremsstrahlung curve? (Y/N): ")[0].lower()
if choice == "y":
    b_curve()