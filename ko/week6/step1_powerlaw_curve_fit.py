"""
Step 1: Power Law Model Curve Fitting
이 스크립트는 가상의 전단 속도(Shear Rate)와 전단 응력(Shear Stress) 데이터를 통해
비뉴턴 유체의 Power Law 모델 (Tau = K * Gamma^n) 계수인
농도 계수(Consistency Index, K)와 유동 지수(Flow Behavior Index, n)를
scipy.optimize.curve_fit을 이용해 산출하는 기본 알고리즘입니다.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False
from scipy.optimize import curve_fit

# 1. 가상의 실험 데이터 보간 (전분 풀 - Pseudoplastic 유체 가정)
# 전단 속도 (Shear Rate, 1/s): 10 ~ 100
shear_rate_data = np.array([10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
# 전단 응력 (Shear Stress, Pa) (측정 결과 가정)
shear_stress_data = np.array([18.5, 29.3, 38.5, 46.8, 54.3, 61.2, 67.8, 74.0, 80.0, 85.8])

# 2. 파워 로우(Power Law) 모델 함수 정의
# 식: \tau = K * \dot{\gamma}^n
def power_law(gamma, K, n):
    return K * (gamma ** n)

# 3. 최적 계수 찾기 (Curve Fitting)
# popt: 최적 피팅 파라미터 [K, n]
# pcov: 파라미터의 공분산 행렬
popt, pcov = curve_fit(power_law, shear_rate_data, shear_stress_data)

K_est, n_est = popt
print(f"--- Power Law 피팅 결과 ---")
print(f"농도 계수 (K): {K_est:.4f} Pa·s^n")
print(f"유동 지수 (n): {n_est:.4f}")

# 4. 결괏값 도식화 및 그래프 모델
shear_rate_smooth = np.linspace(0, 100, 200)
shear_stress_fit = power_law(shear_rate_smooth, K_est, n_est)

plt.figure(figsize=(8, 6))

# 실험 데이터 산점도 (Scatter)
plt.scatter(shear_rate_data, shear_stress_data, color='blue', label='Experimental Data (Starch Paste)', s=50, zorder=3)

# 피팅된 파워 로우 곡선 (Line)
plt.plot(shear_rate_smooth, shear_stress_fit, color='red', linewidth=2, label=rf'Power Law Fit ($\tau = {K_est:.2f} \cdot \dot{{\gamma}}^{{{n_est:.2f}}}$)', zorder=2)

plt.title('Non-Newtonian Fluid: Power Law Curve Fitting', fontsize=14, fontweight='bold')
plt.xlabel('Shear Rate ($\dot{\gamma}$, $s^{-1}$)', fontsize=12)
plt.ylabel('Shear Stress ($\\tau$, Pa)', fontsize=12)
plt.xlim(0, 110)
plt.ylim(0, 100)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend(fontsize=11)

plt.tight_layout()
plt.show()
