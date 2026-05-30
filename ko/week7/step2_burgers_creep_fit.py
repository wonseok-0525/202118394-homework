"""
[Step 2] Burgers Creep Model Curve Fitting
- Week 7 Lab: Viscoelastic Properties — Creep & Stress Relaxation
- 4-parameter (E₁, E₂, η₁, η₂) non-linear inverse estimation based on curve_fit
- Visualization of 3-stage creep decomposition (Instant Elastic + Delayed Elastic + Viscous Flow)
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False
from scipy.optimize import curve_fit

# ============================================================
# 1. Burgers 4-요소 크리프 모델 함수
# ============================================================
SIGMA_0 = 10.0  # 일정 응력 (kPa)

def burgers_creep(t, E1, E2, eta1, eta2):
    """
    Burgers 4-요소 모델 크리프 수식
    ε(t) = σ_0/E_1 + (σ_0/E_2)(1 - exp(-t·E_2/η_2)) + (σ_0/η_1)·t
    """
    instant = SIGMA_0 / E1
    delayed = (SIGMA_0 / E2) * (1 - np.exp(-t * E2 / eta2))
    viscous = (SIGMA_0 / eta1) * t
    return instant + delayed + viscous


# ============================================================
# 2. 가상 크리프 실험 데이터 (사과 Fuji 기반)
# ============================================================
t_data = np.array([0, 2, 5, 10, 20, 30, 45, 60, 90, 120])
strain_data = np.array([2.50, 3.85, 5.10, 6.40, 7.90, 9.05, 10.50, 11.70, 13.80, 15.60])

# ============================================================
# 3. 곡선 피팅 — 4-파라미터 역산
# ============================================================
# 초기 추정값 (물리적 범위 내)
p0 = [200, 100, 5000, 500]
bounds = ([10, 10, 100, 50], [1000, 1000, 50000, 10000])

popt, pcov = curve_fit(burgers_creep, t_data, strain_data, p0=p0, bounds=bounds)
E1_fit, E2_fit, eta1_fit, eta2_fit = popt
perr = np.sqrt(np.diag(pcov))

# R² 산출
strain_pred = burgers_creep(t_data, *popt)
ss_res = np.sum((strain_data - strain_pred) ** 2)
ss_tot = np.sum((strain_data - np.mean(strain_data)) ** 2)
r_squared = 1 - (ss_res / ss_tot)

print("=" * 65)
print("  📈 Burgers 크리프 곡선 피팅 — 7주차 실습 Step 2")
print("=" * 65)
print(f"\n  📌 일정 응력 σ_0 = {SIGMA_0:.1f} kPa")
print(f"\n  {'파라미터':<12} {'피팅값':>12} {'단위':>12} {'표준편차':>12}")
print("-" * 50)
print(f"  {'E_1':12} {E1_fit:12.2f} {'kPa':>12} {perr[0]:12.3f}")
print(f"  {'E_2':12} {E2_fit:12.2f} {'kPa':>12} {perr[1]:12.3f}")
print(f"  {'η_1':12} {eta1_fit:12.2f} {'kPa·s':>12} {perr[2]:12.3f}")
print(f"  {'η_2':12} {eta2_fit:12.2f} {'kPa·s':>12} {perr[3]:12.3f}")
print("-" * 50)
print(f"  Delayed Time τ_c = η_2/E_2 = {eta2_fit/E2_fit:.2f} s")
print(f"  R² = {r_squared:.6f}")
# 💡 Assessment Criteria & Troubleshooting Guide:
# - ✅ Excellent Fit (R² > 0.99): The model describes the experimental data very accurately.
# - ⚠️ Additional Review Required (R² <= 0.99): Please check the following:
#   1) Verify if the initial guesses (p0) are within a reasonable physical range (200, 100, 5000, 500).
#   2) Check for noise or outliers in the experimental data.
#   3) Evaluate if the sample material's behavior is suitable for the Burgers 4-element model.
print(f"  Assessment: {'✅ Excellent Fit' if r_squared > 0.99 else '⚠️ Additional Review Required'}")

# ============================================================
# 4. 시각화 — 피팅 곡선 + 3단계 분해
# ============================================================
t_fine = np.linspace(0, 130, 500)

# 전체 피팅 곡선
strain_fit = burgers_creep(t_fine, *popt)

# 3단계 분해 성분
instant_comp = np.full_like(t_fine, SIGMA_0 / E1_fit)
delayed_comp = instant_comp + (SIGMA_0 / E2_fit) * (1 - np.exp(-t_fine * E2_fit / eta2_fit))
viscous_comp = (SIGMA_0 / eta1_fit) * t_fine

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
fig.suptitle("Burgers 4-Element Creep Model — Curve Fitting & Decomposition",
             fontsize=14, fontweight="bold")

# 좌측: 피팅 결과
ax1.scatter(t_data, strain_data, color="#e74c3c", s=80, zorder=5,
            edgecolors="black", linewidths=0.5, label="실험 데이터")
ax1.plot(t_fine, strain_fit, "b-", linewidth=2.5,
         label=f"Burgers Fit (R²={r_squared:.4f})")
ax1.set_xlabel("Time (s)", fontsize=12)
ax1.set_ylabel("Strain ε (%)", fontsize=12)
ax1.set_title("Creep Curve Fitting", fontsize=12)
ax1.legend(fontsize=10)
ax1.grid(True, alpha=0.3)

# 우측: 3단계 분해
ax2.fill_between(t_fine, 0, instant_comp, alpha=0.3, color="#e74c3c",
                 label=f"① 즉시 탄성 (σ_0/E_1 = {SIGMA_0/E1_fit:.2f}%)")
ax2.fill_between(t_fine, instant_comp, delayed_comp, alpha=0.3, color="#f39c12",
                 label="② 지연 탄성 (KV 요소)")
ax2.fill_between(t_fine, 0, viscous_comp, alpha=0.2, color="#2ecc71",
                 label=f"③ 점성 유동 (기울기={SIGMA_0/eta1_fit:.4f} %/s)")
ax2.plot(t_fine, strain_fit, "k-", linewidth=2, label="총 변형률")
ax2.set_xlabel("Time (s)", fontsize=12)
ax2.set_ylabel("Strain ε (%)", fontsize=12)
ax2.set_title("Creep 3-Component Decomposition", fontsize=12)
ax2.legend(fontsize=9, loc="upper left")
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("step2_result.png", dpi=150, bbox_inches="tight")
plt.show()

print(f"\n   그래프가 step2_result.png 으로 저장됨")
print("=" * 65)
