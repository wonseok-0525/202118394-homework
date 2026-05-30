"""
Step 4: Power Law Model - Dual Axis Analysis (Shear Stress & Apparent Viscosity)
이 스크립트는 전단 속도에 따른 전단 응력(\tau)과 겉보기 점도(\eta)의 변화를
하나의 그래프에 이중 Y축(Dual Y-axis)으로 시각화하여 비뉴턴 유체의 특성을 종합적으로 분석합니다.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 1. 고정 파라미터 설정 (Step 1의 피팅 결과 반영)
K = 4.0160  # 농도 계수 (Pa·s^n)
n = 0.6650  # 유동 지수 (n < 1: 전단 박화 유체)

# 2. 데이터 생성
shear_rate = np.linspace(0.1, 100, 500)  # 전단 속도 (1/s)
shear_stress = K * (shear_rate ** n)     # 전단 응력 (Pa)
apparent_viscosity = K * (shear_rate ** (n - 1))  # 겉보기 점도 (Pa·s)

# 3. 이중 Y축 그래프 시각화
fig, ax1 = plt.subplots(figsize=(10, 6))

# 첫 번째 Y축: 전단 응력 (Shear Stress)
color1 = 'tab:red'
ax1.set_xlabel('Shear Rate ($\dot{\gamma}$, $s^{-1}$)', fontsize=12)
ax1.set_ylabel('Shear Stress ($\\tau$, Pa)', color=color1, fontsize=12)
line1 = ax1.plot(shear_rate, shear_stress, color=color1, lw=2.5, label='Shear Stress ($\\tau$)')
ax1.tick_params(axis='y', labelcolor=color1)
ax1.set_ylim(0, 100)
ax1.grid(True, linestyle='--', alpha=0.5)

# 두 번째 Y축 (오른쪽): 겉보기 점도 (Apparent Viscosity)
ax2 = ax1.twinx()
color2 = 'tab:blue'
ax2.set_ylabel('Apparent Viscosity ($\eta$, Pa·s)', color=color2, fontsize=12)
line2 = ax2.plot(shear_rate, apparent_viscosity, color=color2, lw=2.5, linestyle='--', label='Apparent Viscosity ($\eta$)')
ax2.tick_params(axis='y', labelcolor=color2)
ax2.set_ylim(0, 10)  # 초기 전단 박화 현상을 잘 보여주기 위한 범위 설정

# 범례 통합
lines = line1 + line2
labels = [l.get_label() for l in lines]
ax1.legend(lines, labels, loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=2)

# 그래프 여백 조정
fig.tight_layout()

# 그래프 저장 (선택 사항)
import os
save_path = '../../assets/week6/power_law_model_chart.png'
os.makedirs(os.path.dirname(save_path), exist_ok=True)
plt.savefig(save_path, dpi=300, bbox_inches='tight')

# plt.show()
