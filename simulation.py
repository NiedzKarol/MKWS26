import cantera as ct
import numpy as np
import matplotlib.pyplot as plt

print("Starting combustion simulation using GRI 3.0 mechanism...")

# Wczytanie mechanizmu GRI 3.0 (standard dla metanu)
gas = ct.Solution('gri30.yaml')
pressure = ct.one_atm

# Pobranie indeksu dla NO, aby uniknąć błędów tablic Numpy w nowych wersjach Cantery
idx_NO = gas.species_index('NO')

# ==============================================================================
# PLOT 1: NO formation over time for a specific condition (T=1600K, Phi=1.0)
# ==============================================================================
print("1/3 Generating time-history data for T=1600K, Phi=1.0...")

gas.TP = 1600, pressure
gas.set_equivalence_ratio(1.0, 'CH4', 'O2:0.21, N2:0.79')

# Dodano clone=False zgodnie z wymaganiami nowej Cantery 3.x
r_time = ct.IdealGasConstPressureReactor(gas, clone=False)
sim_time = ct.ReactorNet([r_time])

times = []
no_fractions = []
temp_history = []

time = 0.0
for n in range(200):
    time += 0.0005 # krok 0.5 ms, całkowity czas 0.1 s
    sim_time.advance(time)
    times.append(time * 1000) # czas w milisekundach
    no_fractions.append(gas.X[idx_NO] * 1e6) # Prawidłowe pobieranie ułamka molowego NO w ppm
    temp_history.append(r_time.T)

plt.figure(figsize=(8, 5))
# Dodano literę 'r' przed stringami, aby uniknąć SyntaxWarning
plt.plot(times, no_fractions, 'r-', linewidth=2)
plt.title(r'NO Formation Over Time (T_init = 1600 K, $\Phi$ = 1.0)')
plt.xlabel('Time [ms]')
plt.ylabel('NO Mole Fraction [ppm]')
plt.grid(True)
plt.tight_layout()
plt.savefig('plot_time_history.png', dpi=300)
plt.close()

# ==============================================================================
# PARAMETER SWEEP: Generating data for different Temperatures and Phi
# ==============================================================================
print("2/3 Running parameter sweep for various T and Phi...")

temperatures = np.linspace(1200, 1800, 25)
phis = np.linspace(0.6, 1.4, 25)

# Macierz do przechowywania wyników końcowych
no_matrix = np.zeros((len(phis), len(temperatures)))

for i, phi in enumerate(phis):
    for j, T in enumerate(temperatures):
        gas.TP = T, pressure
        gas.set_equivalence_ratio(phi, 'CH4', 'O2:0.21, N2:0.79')
        
        r = ct.IdealGasConstPressureReactor(gas, clone=False)
        sim = ct.ReactorNet([r])
        sim.advance(0.1) # Czas przebywania: 0.1 s
        
        no_matrix[i, j] = gas.X[idx_NO] * 1e6

# ==============================================================================
# PLOT 2: Final NO emission vs Initial Temperature for specific Phi values
# ==============================================================================
print("Generating Plot 2...")

plt.figure(figsize=(8, 5))
# Wybieramy indeksy z tablicy 'phis' najbliższe wartościom 0.8, 1.0 i 1.2
idx_phi_08 = np.argmin(np.abs(phis - 0.8))
idx_phi_10 = np.argmin(np.abs(phis - 1.0))
idx_phi_12 = np.argmin(np.abs(phis - 1.2))

plt.plot(temperatures, no_matrix[idx_phi_08, :], 'b-o', label=r'$\Phi$ = 0.8 (Lean)')
plt.plot(temperatures, no_matrix[idx_phi_10, :], 'g-s', label=r'$\Phi$ = 1.0 (Stoichiometric)')
plt.plot(temperatures, no_matrix[idx_phi_12, :], 'r-^', label=r'$\Phi$ = 1.2 (Rich)')

plt.title('Effect of Initial Temperature on NO Emission')
plt.xlabel('Initial Temperature [K]')
plt.ylabel('Final NO Emission [ppm]')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig('plot_no_vs_temp.png', dpi=300)
plt.close()

# ==============================================================================
# PLOT 3: Contour map of NO emission vs (Temperature, Phi)
# ==============================================================================
print("3/3 Generating contour map...")

plt.figure(figsize=(8, 6))
T_grid, Phi_grid = np.meshgrid(temperatures, phis)
cp = plt.contourf(T_grid, Phi_grid, no_matrix, levels=25, cmap='jet')
plt.colorbar(cp, label='Final NO Emission [ppm]')

plt.title('NO Emission Map (Residence time = 0.1s)')
plt.xlabel('Initial Temperature [K]')
plt.ylabel(r'Equivalence Ratio ($\Phi$)')
plt.tight_layout()
plt.savefig('plot_contour.png', dpi=300)
plt.close()

print("Simulation finished! Three plots have been generated and saved.")