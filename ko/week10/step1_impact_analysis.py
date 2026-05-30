"""
10주차 실습 Step 1: 과일 낙하 충격 특성 및 반발 계수 분석 (인터랙티브 시뮬레이션)
- 가상의 Tracker 속도 데이터를 기반으로 도출된 반발 계수 활용
- Slider를 통한 질량, 낙하 높이, 손상 임계치 동적 조절
- 완충재 유무에 따른 최대 충격력 비교 및 손상 시뮬레이션
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Slider, Button
import matplotlib.font_manager as fm

# 한글 폰트 설정 (Windows: Malgun Gothic, Mac: AppleGothic)
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# =====================================================================
# 1. 물리 파라미터 및 상수 설정
# =====================================================================
g = 9.81  # 중력 가속도 (m/s^2)

# 기존 Tracker 데이터에서 도출된 반발 계수 (고정값으로 사용)
# 맨바닥: v1 = 4.40, v2 = 1.50 -> e = 0.34
# 완충재: v1 = 4.40, v2 = 0.80 -> e = 0.18
e_hard = 1.50 / 4.40
e_soft = 0.80 / 4.40

# 충돌 지속 시간
dt_hard = 0.005  # s
dt_soft = 0.020  # s

# 초기 상태 변수
init_mass = 0.25
init_drop_height = 1.0
init_bruise_threshold = 150.0

# =====================================================================
# 2. 시뮬레이션 데이터 계산 함수
# =====================================================================
t_total = 1.5  # 전체 시뮬레이션 시간 (최대 2.0m 낙하 고려하여 고정)
fps = 60
num_frames = int(t_total * fps)
time_array = np.linspace(0, t_total, num_frames)

def calculate_data(mass, drop_height):
    v1 = -np.sqrt(2 * g * drop_height)
    v2_hard = abs(v1) * e_hard
    v2_soft = abs(v1) * e_soft
    
    force_hard = mass * (v2_hard - v1) / dt_hard
    force_soft = mass * (v2_soft - v1) / dt_soft
    
    t_fall = np.sqrt(2 * drop_height / g)
    
    y_h = np.zeros(num_frames)
    y_s = np.zeros(num_frames)
    f_h = np.zeros(num_frames)
    f_s = np.zeros(num_frames)
    
    for i, t in enumerate(time_array):
        # 맨바닥 (Hard Surface)
        if t < t_fall:
            y_h[i] = drop_height - 0.5 * g * t**2
        elif t < t_fall + dt_hard:
            y_h[i] = 0
            f_h[i] = force_hard
        else:
            t_b = t - (t_fall + dt_hard)
            y_h[i] = v2_hard * t_b - 0.5 * g * t_b**2
            if y_h[i] < 0: y_h[i] = 0
            
        # 완충재 (Soft Surface)
        if t < t_fall:
            y_s[i] = drop_height - 0.5 * g * t**2
        elif t < t_fall + dt_soft:
            compress = (t - t_fall) / dt_soft
            y_s[i] = -0.05 * np.sin(compress * np.pi)
            f_s[i] = force_soft
        else:
            t_b = t - (t_fall + dt_soft)
            y_s[i] = v2_soft * t_b - 0.5 * g * t_b**2
            if y_s[i] < 0: y_s[i] = 0
            
    return y_h, y_s, f_h, f_s, force_hard, force_soft

# 초기 데이터 계산
y_hard, y_soft, f_hard, f_soft, fh_max, fs_max = calculate_data(init_mass, init_drop_height)

# =====================================================================
# 3. 그래프 및 GUI 레이아웃 설정
# =====================================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))
fig.subplots_adjust(bottom=0.35)  # 슬라이더를 위한 하단 공간 확보
fig.suptitle('[시뮬레이션] 과일 낙하 충격 인터랙티브', fontsize=18, fontweight='bold')

# --- 1) 낙하 애니메이션 축 설정 ---
ax1.set_xlim(-1, 3)
ax1.set_ylim(-0.15, 2.2)  # 최대 높이 2.0m 기준
ax1.set_xticks([0, 2])
ax1.set_xticklabels(['맨바닥 (Hard)', '완충재 적용 (Soft)'], fontsize=12)
ax1.set_ylabel('높이 (m)', fontsize=12)
ax1.set_title('낙하 및 반발 애니메이션', fontsize=14)
ax1.grid(True, linestyle='--', alpha=0.6)

# 바닥 및 완충재 시각화
ax1.axhline(0, color='black', linewidth=3)
ax1.axhline(-0.05, xmin=0.6, xmax=0.9, color='lightgreen', linewidth=10, alpha=0.5)

apple_hard, = ax1.plot([], [], 'ro', markersize=20, label='사과 (맨바닥)')
apple_soft, = ax1.plot([], [], 'go', markersize=20, label='사과 (완충재)')
ax1.legend(loc='upper right')

# --- 2) 충격력 그래프 축 설정 ---
ax2.set_xlim(0, t_total)
ax2.set_ylim(0, 900)  # 발생 가능한 최대 충격력 기준 넉넉하게 설정
ax2.set_xlabel('시간 (s)', fontsize=12)
ax2.set_ylabel('충격력 (N)', fontsize=12)
ax2.set_title('시간에 따른 충격력 변화', fontsize=14)
ax2.grid(True, linestyle='--', alpha=0.6)

thresh_line = ax2.axhline(init_bruise_threshold, color='red', linestyle='--', linewidth=2, label=f'멍 발생 한계 ({init_bruise_threshold}N)')
line_f_hard, = ax2.plot([], [], 'r-', linewidth=3, label='맨바닥 충격력')
line_f_soft, = ax2.plot([], [], 'g-', linewidth=3, label='완충재 충격력')
ax2.legend(loc='upper right')

# 정보 표시용 텍스트 박스
bbox_props_hard = dict(boxstyle="round,pad=0.5", fc="white", ec="red", lw=2, alpha=0.8)
bbox_props_soft = dict(boxstyle="round,pad=0.5", fc="white", ec="green", lw=2, alpha=0.8)

txt_hard = ax2.text(0.05, 0.85, '', transform=ax2.transAxes, fontsize=12, fontweight='bold', bbox=bbox_props_hard)
txt_soft = ax2.text(0.05, 0.70, '', transform=ax2.transAxes, fontsize=12, fontweight='bold', bbox=bbox_props_soft)

# =====================================================================
# 4. UI 컨트롤 (슬라이더 및 버튼)
# =====================================================================
axcolor = 'lightgray'
ax_mass = plt.axes([0.15, 0.20, 0.65, 0.03], facecolor=axcolor)
ax_height = plt.axes([0.15, 0.15, 0.65, 0.03], facecolor=axcolor)
ax_thresh = plt.axes([0.15, 0.10, 0.65, 0.03], facecolor=axcolor)

s_mass = Slider(ax_mass, '사과 질량 (kg)', 0.1, 0.5, valinit=init_mass, valstep=0.01)
s_height = Slider(ax_height, '낙하 높이 (m)', 0.5, 2.0, valinit=init_drop_height, valstep=0.1)
s_thresh = Slider(ax_thresh, '손상 임계치 (N)', 50, 800, valinit=init_bruise_threshold, valstep=10)

btn_ax = plt.axes([0.85, 0.15, 0.1, 0.08])
btn_restart = Button(btn_ax, '다시 재생\n(Restart)', hovercolor='white')

current_frame = [0]

def update_sliders(val=None):
    global y_hard, y_soft, f_hard, f_soft
    m = s_mass.val
    h = s_height.val
    thresh = s_thresh.val
    
    # 변경된 값으로 데이터 재계산
    y_hard, y_soft, f_hard, f_soft, fh, fs = calculate_data(m, h)
    
    # 임계치 선 및 범례 업데이트
    thresh_line.set_ydata([thresh, thresh])
    thresh_line.set_label(f'멍 발생 한계 ({thresh:.0f}N)')
    ax2.legend(loc='upper right')
    
    # 텍스트 박스 업데이트
    txt_hard.set_text(f"맨바닥 최대 충격: {fh:.1f} N\n({'손상 발생 (X)' if fh > thresh else '안전 (O)'})")
    txt_hard.set_color('darkred' if fh > thresh else 'darkgreen')
    
    txt_soft.set_text(f"완충재 최대 충격: {fs:.1f} N\n({'손상 발생 (X)' if fs > thresh else '안전 (O)'})")
    txt_soft.set_color('darkred' if fs > thresh else 'darkgreen')
    
    # 애니메이션 프레임 초기화
    current_frame[0] = 0

# 슬라이더 값 변경 시 이벤트 연결
s_mass.on_changed(update_sliders)
s_height.on_changed(update_sliders)
s_thresh.on_changed(update_sliders)

def restart_anim(event):
    current_frame[0] = 0

btn_restart.on_clicked(restart_anim)

# 초기 텍스트 설정 적용
update_sliders()

# =====================================================================
# 5. 애니메이션 루프
# =====================================================================
def frame_generator():
    while True:
        yield current_frame[0]
        # 마지막 프레임에 도달하면 멈춰 있도록 함
        if current_frame[0] < num_frames - 1:
            current_frame[0] += 1

def update_anim(f):
    apple_hard.set_data([0], [y_hard[f]])
    apple_soft.set_data([2], [y_soft[f]])
    
    line_f_hard.set_data(time_array[:f+1], f_hard[:f+1])
    line_f_soft.set_data(time_array[:f+1], f_soft[:f+1])
    
    return apple_hard, apple_soft, line_f_hard, line_f_soft, thresh_line, txt_hard, txt_soft

ani = animation.FuncAnimation(
    fig, update_anim, frames=frame_generator, 
    interval=1000/fps, blit=False, cache_frame_data=False
)

plt.show()
