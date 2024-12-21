import matplotlib.pyplot as plt
import numpy as np

# Generate random data for frequency and impedance
frequency = np.linspace(2, 10, 25)  # Frequency from 2 GHz to 10 GHz (100 points)

# Generate random impedance data
real_impedance_sim = np.abs(10 + 20 * np.sin(0.5 * np.pi * frequency))
real_impedance_cal_1nH = np.abs(10 + 18 * np.cos(0.4 * np.pi * frequency))
real_impedance_cal_100nH = np.abs(50 + 5 * np.sin(0.3 * np.pi * frequency))

imag_impedance_sim = -100 + 20 * np.cos(0.5 * np.pi * frequency)
imag_impedance_cal_1nH = -90 + 25 * np.sin(0.4 * np.pi * frequency)
imag_impedance_cal_100nH = -80 + 30 * np.cos(0.3 * np.pi * frequency)

# Set global parameters for thicker lines and larger fonts
plt.rcParams['axes.linewidth'] = 1.5  # Thickness of the axis lines
plt.rcParams['xtick.major.width'] = 1.5  # Thickness of major x-axis ticks
plt.rcParams['ytick.major.width'] = 1.5  # Thickness of major y-axis ticks
plt.rcParams['font.size'] = 14         # Font size for labels and titles

# Create the plot
plt.figure(figsize=(12, 6))

# Plot the real part of impedance
plt.subplot(1, 2, 1)
plt.plot(frequency, real_impedance_sim, 'r-o', linewidth=2, markersize=10, label=r'$\mathbf{Re(Z_{in})\ Sim,\ L_D=1\ nH}$')
plt.plot(frequency, real_impedance_cal_1nH, 'g-o', linewidth=2, markersize=10, label=r'$\mathbf{Re(Z_{in})\ Cal,\ L_D=1\ nH}$')
plt.plot(frequency, real_impedance_cal_100nH, 'b-^', linewidth=2, markersize=10, label=r'$\mathbf{Re(Z_{in})\ Cal,\ L_D=100\ nH}$')
plt.xlabel(r'$\mathbf{Frequency\ (GHz)}$')
plt.ylabel(r'$\mathbf{Impedance\ (\Omega)}$')
plt.title(r'$\mathbf{Real\ Part\ of\ Impedance}$')
plt.legend()
plt.grid(True)

# Plot the imaginary part of impedance
plt.subplot(1, 2, 2)
plt.plot(frequency, imag_impedance_sim, 'r-o', linewidth=2, markersize=10, label=r'$\mathbf{Im(Z_{in})\ Sim,\ L_D=1\ nH}$')
plt.plot(frequency, imag_impedance_cal_1nH, 'g-o', linewidth=2, markersize=10, label=r'$\mathbf{Im(Z_{in})\ Cal,\ L_D=1\ nH}$')
plt.plot(frequency, imag_impedance_cal_100nH, 'b-^', linewidth=2, markersize=10, label=r'$\mathbf{Im(Z_{in})\ Cal,\ L_D=100\ nH}$')
plt.xlabel(r'$\mathbf{Frequency\ (GHz)}$')
plt.ylabel(r'$\mathbf{Impedance\ (\Omega)}$')
plt.title(r'$\mathbf{Imaginary\ Part\ of\ Impedance}$')
plt.legend()
plt.grid(True)

# Adjust layout and show the plot
plt.tight_layout()
plt.show()
