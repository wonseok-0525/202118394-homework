"""
Step 2: Apparent Viscosity Dynamics Simulation
이 스크립트는 슬라이더 UI를 통해 유동 지수(n)를 실시간으로 조작하여,
비뉴턴 유체(Pseudoplastic, Newtonian, Dilatant)의 겉보기 점도(Apparent Viscosity)가 
전단 속도에 따라 어떻게 급감, 유지, 폭증하는지 시뮬레이션합니다.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False
from matplotlib.widgets import Slider

# 1. 초기 파라미터 설정 및 배열 생성
initial_K = 10.0   # 초기 농도 계수 (Pa·s^n)
initial_n = 0.5    # 초기 유동 지수 (Pseudoplastic)

shear_rate = np.linspace(0.1, 100, 500)  # 분모의 0 방지를 위해 0.1부터 시작

def calc_apparent_viscosity(K, n, gamma):
    # \eta = \frac{\tau}{\dot{\gamma}} = K \cdot \dot{\gamma}^{n-1}
    return K * (gamma ** (n - 1))

# 초기 결과 계산
app_viscosity = calc_apparent_viscosity(initial_K, initial_n, shear_rate)

# 2. 그래프 및 UI 레이아웃 설정
fig, ax = plt.subplots(figsize=(10, 7))
plt.subplots_adjust(bottom=0.25, top=0.9)
fig.tight_layout(rect=[0, 0.25, 1, 1])  # 슬라이더 공간 확보

# 그래프 플롯팅
line, = ax.plot(shear_rate, app_viscosity, color='purple', lw=3)
ax.set_title(f"Apparent Viscosity vs Shear Rate (n = {initial_n:.2f})", fontsize=14, fontweight='bold')
ax.set_xlabel('Shear Rate ($\dot{\gamma}$, $s^{-1}$)', fontsize=12)
ax.set_ylabel('Apparent Viscosity ($\eta$, Pa·s)', fontsize=12)

# y축은 시인성을 위해 로그 스케일 권장 또는 범위 한정 필요
ax.set_ylim(0, 50)
ax.set_xlim(0, 100)
ax.grid(True, linestyle='--', alpha=0.7)

# 구분선 (기준선)
ax.axhline(initial_K, color='gray', linestyle=':', label='n=1.0 (Newtonian) Reference')
ax.legend()

# 3. 슬라이더 위젯 설정
ax_n = plt.axes([0.15, 0.1, 0.70, 0.03], facecolor='lightgoldenrodyellow')
slider_n = Slider(
    ax=ax_n,
    label='Flow Index (n)',
    valmin=0.2,   # 극단적 전단 박화
    valmax=1.8,   # 전단 농화
    valinit=initial_n,
    valstep=0.05
)

def get_fluid_type(n_val):
    if n_val < 0.95: return "Pseudoplastic (Shear Thinning)"
    elif n_val > 1.05: return "Dilatant (Shear Thickening)"
    else: return "Newtonian Fluid"

# 4. 슬라이더 업데이트 함수
def update(val):
    current_n = slider_n.val
    
    # 겉보기 점도 실시간 재계산
    new_viscosity = calc_apparent_viscosity(initial_K, current_n, shear_rate)
    
    # y 데이터 갱신
    line.set_ydata(new_viscosity)
    ax.set_title(f"{get_fluid_type(current_n)}: Apparent Viscosity Dynamics (n = {current_n:.2f})", fontsize=14, fontweight='bold')
    
    # 극단적 값일 때의 Y 범위 재조절
    if current_n > 1.05:
        ax.set_ylim(0, max(new_viscosity) + 10)
    elif current_n < 0.95:
        ax.set_ylim(0, 50)
    else:
        ax.set_ylim(0, 20)
        
    fig.canvas.draw_idle()

slider_n.on_changed(update)

plt.show()
