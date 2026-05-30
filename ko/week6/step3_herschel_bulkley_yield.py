"""
Step 3: Herschel-Bulkley Yield Stress Analysis
초기 유동을 일으키기 위해 최소한의 항복 응력(Yield Stress)을 필요로 하는
토마토 페이스트, 마요네즈 등의 비뉴턴 유체 거동을 파악하고 최적화 스크롤을 구동합니다.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False
from matplotlib.widgets import Slider

# 1. 초기 변수
initial_tau_y = 20.0  # 항복 응력 (Pa)
initial_K = 5.0       # 농도 계수
initial_n = 0.6       # 유동 지수 (주로 n < 1 인 전단 박화 현상 동반)

shear_rate = np.linspace(0, 100, 500)

def herschel_bulkley(gamma, tau_y, K, n):
    # \tau = \tau_y + K * \dot{\gamma}^n
    stress = np.zeros_like(gamma)
    # 전단 속도가 0보다 클 때만 응력 발생, 0일 때는 tau_y까지만 버팀
    mask = gamma > 0
    stress[mask] = tau_y + K * (gamma[mask] ** n)
    stress[~mask] = tau_y
    return stress

initial_stress = herschel_bulkley(shear_rate, initial_tau_y, initial_K, initial_n)

# 2. 메인 플롯 설정
fig, ax = plt.subplots(figsize=(10, 7))
plt.subplots_adjust(bottom=0.3, top=0.9)

line, = ax.plot(shear_rate, initial_stress, color='darkorange', lw=3, label='Herschel-Bulkley Model')
ax.set_title('Bingham Plastic / Yield-Stress Fluid Behavior', fontsize=14, fontweight='bold')
ax.set_xlabel('Shear Rate ($\dot{\gamma}$, $s^{-1}$)', fontsize=12)
ax.set_ylabel('Shear Stress ($\\tau$, Pa)', fontsize=12)

ax.set_xlim(0, 100)
ax.set_ylim(0, 150)
ax.grid(True, linestyle='--', alpha=0.7)

# 빙햄 가소성 모델의 특징인 'Y 절편' 표시를 위한 수평선
hline = ax.axhline(initial_tau_y, color='red', linestyle=':', label=f'Yield Stress = {initial_tau_y} Pa')
ax.legend(loc='upper left')

# 3. 슬라이더 설정
ax_tau = plt.axes([0.2, 0.15, 0.65, 0.03], facecolor='lightgray')
ax_n   = plt.axes([0.2, 0.08, 0.65, 0.03], facecolor='lightgray')

slider_tau = Slider(ax_tau, 'Yield Stress ($\\tau_y$)', 0.0, 50.0, valinit=initial_tau_y)
slider_n   = Slider(ax_n, 'Flow Index (n)', 0.3, 1.5, valinit=initial_n)

# 4. 실시간 콜백 업데이트
def update(val):
    c_tau_y = slider_tau.val
    c_n = slider_n.val
    
    new_stress = herschel_bulkley(shear_rate, c_tau_y, initial_K, c_n)
    
    line.set_ydata(new_stress)
    hline.set_ydata([c_tau_y, c_tau_y])
    hline.set_label(f'Yield Stress = {c_tau_y:.1f} Pa')
    
    ax.legend(loc='upper left')
    fig.canvas.draw_idle()

slider_tau.on_changed(update)
slider_n.on_changed(update)

plt.show()
