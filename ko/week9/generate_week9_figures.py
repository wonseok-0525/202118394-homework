import numpy as np
import matplotlib.pyplot as plt
import os
import matplotlib.font_manager as fm

plt.style.use('seaborn-v0_8-whitegrid')
# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

save_dir = '../../assets/week9'
os.makedirs(save_dir, exist_ok=True)

# 1-1. stress_strain_basics.png
fig, ax = plt.subplots(figsize=(8, 5))
strain = np.linspace(0, 0.2, 200)
# Linear elastic
elastic_mask = strain <= 0.05
# Plastic
plastic_mask = (strain > 0.05) & (strain <= 0.15)
# Failure
failure_mask = strain > 0.15

stress = np.zeros_like(strain)
stress[elastic_mask] = strain[elastic_mask] * 1000
stress[plastic_mask] = 50 + 200 * (strain[plastic_mask] - 0.05) - 2000 * (strain[plastic_mask] - 0.05)**2
stress[failure_mask] = stress[plastic_mask][-1] - 500 * (strain[failure_mask] - 0.15)**2

ax.plot(strain, stress, '#2980b9', lw=3)
ax.axvline(x=0.05, color='gray', linestyle='--', alpha=0.7)
ax.text(0.025, 20, '탄성 구간\n(Elastic)', ha='center', fontsize=12)
ax.text(0.1, 40, '소성 구간\n(Plastic)', ha='center', fontsize=12)
ax.plot([0.05], [50], 'ro', markersize=8)
ax.text(0.045, 52, '항복점 (Yield Point)', ha='right', color='#c0392b', fontsize=12, fontweight='bold')
ax.set_title('응력-변형률 곡선 (Stress-Strain Curve)', fontsize=14, fontweight='bold')
ax.set_xlabel('변형률 ($\epsilon$)', fontsize=12)
ax.set_ylabel('응력 ($\sigma$, MPa)', fontsize=12)
ax.set_xlim(0, 0.18)
ax.set_ylim(0, 60)
plt.tight_layout()
plt.savefig(os.path.join(save_dir, 'stress_strain_basics.png'), dpi=300)
plt.close()

# 1-2. bio_yield_point.png
fig, ax = plt.subplots(figsize=(8, 5))
deformation = np.linspace(0, 5, 200)
force = np.where(deformation < 2, 5 * deformation, 
                 10 + 2 * (deformation - 2) - 0.5 * (deformation - 2)**2)
force = np.where(deformation > 3.5, force - 2*(deformation-3.5), force)

ax.plot(deformation, force, '#27ae60', lw=3)
ax.plot([2], [10], 'ro', markersize=8)
ax.annotate('Bio-yield Point\n(초기 미세 손상 / 좌굴)', xy=(2, 10), xytext=(0.5, 12),
            arrowprops=dict(facecolor='#c0392b', shrink=0.05, width=2, headwidth=8),
            fontsize=12, color='#c0392b', fontweight='bold')
ax.plot([3.5], [11.875], 'ko', markersize=8)
ax.annotate('Rupture Point\n(파괴점)', xy=(3.5, 11.875), xytext=(3.5, 8),
            arrowprops=dict(facecolor='black', shrink=0.05, width=2, headwidth=8),
            fontsize=12, fontweight='bold')
ax.set_title('생물체 압축 곡선 (과일 압축 시험)', fontsize=14, fontweight='bold')
ax.set_xlabel('침투 깊이 ($\delta$, mm)', fontsize=12)
ax.set_ylabel('압축력 ($F$, N)', fontsize=12)
ax.set_ylim(0, 15)
ax.set_xlim(0, 5)
plt.tight_layout()
plt.savefig(os.path.join(save_dir, 'bio_yield_point.png'), dpi=300)
plt.close()

# 1-3. hertz_contact_concept.png
fig, ax = plt.subplots(figsize=(8, 6))
circle1 = plt.Circle((0, 2), 2, color='#3498db', alpha=0.3, ec='#2980b9', lw=2)
circle2 = plt.Circle((0, -3), 3, color='#2ecc71', alpha=0.3, ec='#27ae60', lw=2)
ax.add_patch(circle1)
ax.add_patch(circle2)
ax.plot([-1.2, 1.2], [0, 0], '#c0392b', lw=4, label='접촉면')
ax.annotate('접촉 폭 $2a$', xy=(1.2, 0), xytext=(2.5, 0),
            arrowprops=dict(arrowstyle='->', color='#c0392b', lw=1.5), fontsize=12, color='#c0392b', fontweight='bold')
ax.text(0, 2.5, '구형 1\n(반경 $R_1$, 탄성계수 $E_1$)', ha='center', va='center', fontsize=12, fontweight='bold')
ax.text(0, -3.5, '구형 2\n(반경 $R_2$, 탄성계수 $E_2$)', ha='center', va='center', fontsize=12, fontweight='bold')
ax.set_xlim(-4, 4)
ax.set_ylim(-7, 5)
ax.set_aspect('equal')
ax.axis('off')
ax.set_title('헤르츠 접촉 (Hertz Contact) 개념도', fontsize=14, fontweight='bold', y=0.95)
plt.tight_layout()
plt.savefig(os.path.join(save_dir, 'hertz_contact_concept.png'), dpi=300)
plt.close()

# 1-5. bruise_mechanism.png
fig, ax = plt.subplots(figsize=(8, 6))
z = np.linspace(0, 3, 200)
a = 1.0 # arbitrary contact radius
# Simplified subsurface stress approx
tau = (z/a) * np.exp(-(z/a - 0.48)**2 * 3) * 0.5 
ax.plot(tau, z, '#8e44ad', lw=3)
ax.axhline(y=0.48*a, color='#e74c3c', linestyle='--', lw=2)
ax.text(0.18, 0.48*a - 0.1, '최대 전단 응력 발생 지점\n($z \\approx 0.48a$)', 
        color='#c0392b', fontsize=12, fontweight='bold')
ax.fill_betweenx(z, 0, tau, color='#9b59b6', alpha=0.3)
ax.invert_yaxis()
ax.set_ylabel('표면으로부터의 깊이 ($z$)', fontsize=12)
ax.set_xlabel('내부 전단 응력 ($\\tau$)', fontsize=12)
ax.set_title('접촉면 아래 깊이에 따른 내부 전단 응력 분포', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig(os.path.join(save_dir, 'bruise_mechanism.png'), dpi=300)
plt.close()

print("Week 9 figures generated successfully in assets/week9/")
