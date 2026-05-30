import numpy as np
import matplotlib.pyplot as plt
import os

save_dir = '../../assets/week7'
os.makedirs(save_dir, exist_ok=True)

# Use a professional style
plt.style.use('seaborn-v0_8-whitegrid')

# 1-1. viscoelastic_concept.png
fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(8, 10), sharex=True)
t = np.linspace(0, 10, 500)
# Stress input
stress = np.where((t >= 1) & (t <= 5), 1, 0)
ax1.plot(t, stress, color='#e74c3c', lw=2.5)
ax1.set_ylabel('Stress ($\sigma$)', fontsize=11, fontweight='bold')
ax1.set_title('1. Step Stress Input (Load applied at t=1, removed at t=5)', fontsize=12, fontweight='bold')

# Elastic response
elastic = np.where((t >= 1) & (t <= 5), 1, 0)
ax2.plot(t, elastic, color='#3498db', lw=2.5)
ax2.set_ylabel('Strain ($\epsilon$)', fontsize=11, fontweight='bold')
ax2.set_title('2. Elastic Response (Ideal Solid - Instantaneous)', fontsize=12, fontweight='bold')

# Viscous response
viscous = np.zeros_like(t)
for i in range(1, len(t)):
    viscous[i] = viscous[i-1] + (1 if 1 <= t[i] <= 5 else 0) * 0.02
ax3.plot(t, viscous, color='#9b59b6', lw=2.5)
ax3.set_ylabel('Strain ($\epsilon$)', fontsize=11, fontweight='bold')
ax3.set_title('3. Viscous Response (Ideal Fluid - Permanent Deformation)', fontsize=12, fontweight='bold')

# Viscoelastic response
viscoel = np.zeros_like(t)
for i, time in enumerate(t):
    if time < 1:
        viscoel[i] = 0
    elif time <= 5:
        viscoel[i] = 0.4 + 0.4 * (1 - np.exp(-(time - 1) / 0.8)) + 0.05 * (time - 1)
    else:
        viscoel[i] = 0.05 * 4 + 0.4 * (1 - np.exp(-4 / 0.8)) * np.exp(-(time - 5) / 0.8)
ax4.plot(t, viscoel, color='#2ecc71', lw=2.5)
ax4.set_ylabel('Strain ($\epsilon$)', fontsize=11, fontweight='bold')
ax4.set_title('4. Viscoelastic Response (Combined elastic + viscous)', fontsize=12, fontweight='bold')
ax4.set_xlabel('Time (t)', fontsize=11, fontweight='bold')

plt.tight_layout()
plt.savefig(f'{save_dir}/viscoelastic_concept.png', dpi=300)
plt.close()

# 1-2. creep_relaxation_curves.png
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
t = np.linspace(0, 10, 200)

# Creep
creep = 1 - np.exp(-t/2) + 0.1*t
ax1.plot(t, creep, color='#2980b9', lw=3)
ax1.set_title('Creep Curve (Constant Stress $\sigma_0$)', fontsize=14, fontweight='bold')
ax1.set_xlabel('Time (t)', fontsize=12)
ax1.set_ylabel('Strain ($\epsilon$)', fontsize=12)

# Relaxation
relax = 0.2 + 0.8 * np.exp(-t/1.5)
ax2.plot(t, relax, color='#c0392b', lw=3)
ax2.set_title('Stress Relaxation Curve (Constant Strain $\epsilon_0$)', fontsize=14, fontweight='bold')
ax2.set_xlabel('Time (t)', fontsize=12)
ax2.set_ylabel('Stress ($\sigma$)', fontsize=12)

plt.tight_layout()
plt.savefig(f'{save_dir}/creep_relaxation_curves.png', dpi=300)
plt.close()

# 1-4. maxwell_model_curves.png
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
t = np.linspace(0, 10, 200)

# Stress Relaxation
ax1.plot(t, np.exp(-t/2), color='#c0392b', lw=3)
ax1.set_title('Maxwell: Stress Relaxation (Realistic)', fontsize=14, fontweight='bold')
ax1.set_xlabel('Time (t)', fontsize=12)
ax1.set_ylabel('Stress ($\sigma$)', fontsize=12)
ax1.axhline(0, color='black', lw=1)

# Creep
ax2.plot(t, 1 + 0.2*t, color='#2980b9', lw=3)
ax2.set_title('Maxwell: Creep (Unrealistic linear trend)', fontsize=14, fontweight='bold')
ax2.set_xlabel('Time (t)', fontsize=12)
ax2.set_ylabel('Strain ($\epsilon$)', fontsize=12)

plt.tight_layout()
plt.savefig(f'{save_dir}/maxwell_model_curves.png', dpi=300)
plt.close()

# 1-5. kelvin_voigt_model_curves.png
fig, ax = plt.subplots(figsize=(6, 5))
t = np.linspace(0, 10, 200)
ax.plot(t, 1 - np.exp(-t/2), color='#27ae60', lw=3)
ax.set_title('Kelvin-Voigt: Creep (Saturation curve)', fontsize=14, fontweight='bold')
ax.set_xlabel('Time (t)', fontsize=12)
ax.set_ylabel('Strain ($\epsilon$)', fontsize=12)

plt.tight_layout()
plt.savefig(f'{save_dir}/kelvin_voigt_model_curves.png', dpi=300)
plt.close()

# 1-6. burgers_model_breakdown.png
fig, ax = plt.subplots(figsize=(10, 6))
t = np.linspace(0, 10, 200)
instant = np.ones_like(t) * 0.5
delayed = 0.5 * (1 - np.exp(-t/1.5))
viscous = 0.1 * t
total = instant + delayed + viscous

ax.plot(t, total, 'k-', lw=3, label='Total Strain')
ax.fill_between(t, 0, instant, color='#3498db', alpha=0.4, label='Immediate Elastic ($E_1$)')
ax.fill_between(t, instant, instant+delayed, color='#2ecc71', alpha=0.4, label='Delayed Elastic ($E_2, \eta_2$)')
ax.fill_between(t, instant+delayed, total, color='#9b59b6', alpha=0.4, label='Viscous Flow ($\eta_1$)')

ax.set_title('Burgers Model: Creep Strain Breakdown', fontsize=16, fontweight='bold')
ax.set_xlabel('Time (t)', fontsize=12)
ax.set_ylabel('Strain ($\epsilon$)', fontsize=12)
ax.legend(loc='upper left', fontsize=11)

plt.tight_layout()
plt.savefig(f'{save_dir}/burgers_model_breakdown.png', dpi=300)
plt.close()

print("All figures generated successfully.")
