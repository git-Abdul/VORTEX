import math
import sqlite3
import numpy as np
import matplotlib.pyplot as plt

"""
~ Assumptions: 
   [1] Beam provides 1000 electrons/sec (Ro)
   [2] Energy of the beam ≃ 1GeV (Eo)
   [3] Radius of the beam = 2cm (r)
"""

cursor = sqlite3.connect('elements.db').cursor()

def convert_unit(value: int, type: str):
    if type == "frequency":
        return value*math.pow(10,15) # In Hertz
    elif type == "energy":
        return value*1000*1.602*math.pow(10,-19) # In joules

element_name = input("Enter the name of the element: ").lower().capitalize()
cursor.execute(f"SELECT energy, f_yield FROM elements WHERE name = ?", (element_name,))
value = cursor.fetchall()

energy = value[0][0]
y = value[0][1] # Yield
frequency = energy*1000*1.602/6.626 # Frequency in PHz
power = 1.602*math.pow(10,-6) # Power of the beam: Rate of electrons*(Energy of 1 electron at 1GeV)
area = 0.02*0.02*np.pi
intensity = y*power/area
amplitude = math.sqrt(2*intensity/(3*8.85*math.pow(10,-4)))
print(round(frequency, 2))

x = np.linspace(0, 4 * np.pi, 10000000) # To plot a smoother graph
y = amplitude*np.sin(2*np.pi*frequency*x)

plt.plot(x, y)
if len(str(round(frequency))) > 4:
    plt.xlim(0, 0.0005)
else:
    plt.xlim(0, 0.005)
    
plt.ylim(-1.5, 1.5)

plt.xlabel("Time (fsec)")
plt.ylabel("Amplitude (V/m)")
plt.title(f"X-ray generated using {element_name}")

plt.grid(True, which='both')
plt.axhline(y=0, color='k')

plt.show()
