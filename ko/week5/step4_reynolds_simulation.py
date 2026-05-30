"""
5주차 실습: Step 4 - 레이놀즈 수(Reynolds Number) 유동 상태 파티클 애니메이션 시뮬레이터
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider

# 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 고정 파라미터: 사과즙 농축액 밀도
rho = 1050  # kg/m^3

fig, ax = plt.subplots(figsize=(10, 7))
plt.subplots_adjust(bottom=0.35, top=0.82)

ax.set_xlim(0, 10)
ax.set_ylim(-1.5, 1.5)
ax.set_title('유동 상태 시뮬레이션 (층류 vs 난류)', fontsize=16, fontweight='bold', pad=35)
ax.set_yticks([])
ax.set_xticks([])

# 파이프 경계선 시각화
ax.axhline(1, color='black', lw=6)
ax.axhline(-1, color='black', lw=6)
ax.fill_between([0, 10], 1, 1.1, color='gray', alpha=0.5)
ax.fill_between([0, 10], -1.1, -1, color='gray', alpha=0.5)

# 파티클 초기화 생성
num_particles = 400
x = np.random.uniform(0, 10, num_particles)
y = np.random.uniform(-0.95, 0.95, num_particles)

scatter = ax.scatter(x, y, s=15, c='blue', alpha=0.6)

# UI 슬라이더 영역 설정
ax_v = plt.axes([0.15, 0.20, 0.7, 0.03])
ax_d = plt.axes([0.15, 0.15, 0.7, 0.03])
ax_mu = plt.axes([0.15, 0.10, 0.7, 0.03])

# 슬라이더 생성 (초기값은 천이 구역 근처로 설정 1.5m/s, 0.05m, 0.03Pa.s -> Re=2625)
s_v = Slider(ax_v, '유속 $v$ (m/s)', 0.1, 5.0, valinit=1.5)
s_d = Slider(ax_d, '파이프 내경 $D$ (m)', 0.01, 0.2, valinit=0.05)
s_mu = Slider(ax_mu, r'점도 $\mu$ (Pa.s)', 0.001, 0.1, valinit=0.03)

# 텍스트 상태 표시기
text_re = ax.text(0.5, 1.05, '', transform=ax.transAxes, ha='center', fontsize=15, fontweight='bold')
text_desc = ax.text(0.5, -0.1, '', transform=ax.transAxes, ha='center', fontsize=12, color='dimgray')

def update_text(val):
    v = s_v.val
    d = s_d.val
    mu = s_mu.val
    Re = (rho * v * d) / mu
    
    if Re < 2100:
        state = "층류 (Laminar)"
        color = "blue"
        desc = "유체가 평행하게 흘러 펌프 전력은 절약되나, 파이프 중앙-벽면 간 강제 믹싱(Mixing)이 없어 열교환 효율이 저조합니다."
    elif Re < 4000:
        state = "천이 구역 (Transition)"
        color = "purple"
        desc = "층류에서 난류로 불안정하게 전환되는 영역입니다."
    else:
        state = "난류 (Turbulent)"
        color = "red"
        desc = "강력한 와류(Vortex)가 발생하여 마찰 저항은 커지지만, 상하좌우 강제 믹싱으로 살균(열교환) 효율은 압도적으로 상승합니다!"
        
    text_re.set_text(f"레이놀즈 수 (Re): {Re:,.0f} -> {state}")
    text_re.set_color(color)
    text_desc.set_text(desc)

# 슬라이더 이벤트 연결
s_v.on_changed(update_text)
s_d.on_changed(update_text)
s_mu.on_changed(update_text)

def animate(frame):
    v_avg = s_v.val
    d = s_d.val
    mu = s_mu.val
    Re = (rho * v_avg * d) / mu
    
    global x, y
    
    if Re < 2100:
        # 층류: 중심에서 가장 빠르고 벽면에서 0에 가까운 포물선형 속도 분포
        v_local = 2 * v_avg * (1 - y**2)
        dy = 0
    elif Re < 4000:
        # 천이 구역: 약간의 와류
        v_local = v_avg * (1 - y**2)**0.5
        dy = np.random.normal(0, 0.03 * v_avg, num_particles)
    else:
        # 난류: 전체적으로 거칠고 균일한 속도 분포 + 강력한 랜덤 난류 와류 분산
        v_local = v_avg * np.ones_like(y)
        dy = np.random.normal(0, 0.25 * v_avg, num_particles)
        
    # 가시성을 위해 X축 변위 스케일 조정계수 반영
    dx = v_local * 0.1
    
    x += dx
    y += dy
    
    # 튕겨나가는 파티클 파이프 벽면에서 반사 블록 처리
    y = np.clip(y, -0.96, 0.96)
    
    # 파이프를 통과한 파티클 앞부분으로 리스폰
    out_of_bounds = x > 10
    x[out_of_bounds] = 0
    y[out_of_bounds] = np.random.uniform(-0.95, 0.95, np.sum(out_of_bounds))
    
    # 색상 업데이트
    if Re < 2100:
        scatter.set_color('blue')
    elif Re < 4000:
        scatter.set_color('purple')
    else:
        scatter.set_color('red')
        
    scatter.set_offsets(np.c_[x, y])
    return scatter,

ani = FuncAnimation(fig, animate, frames=200, interval=50, blit=False)

update_text(0)
plt.show()
