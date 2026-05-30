"""
5주차 실습: Step 3 - 배관 직경(D) 최적화 및 하겐-푸아죄유 수식 연계 경제성 시뮬레이터
(토론 2 해설용 애니메이션)
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import matplotlib.patches as patches

# 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

fig = plt.figure(figsize=(12, 7))
plt.subplots_adjust(left=0.08, bottom=0.35, right=0.95, top=0.9, wspace=0.3, hspace=0.3)

# Subplot 1: 배관 단면도 및 압력 저항 벡터 시각화
ax_pipe = plt.subplot(1, 2, 1)
ax_pipe.set_xlim(-0.15, 0.15)
ax_pipe.set_ylim(-0.15, 0.15)
ax_pipe.set_aspect('equal')
ax_pipe.set_title('파이프 단면 및 마찰 점성 저항 (ΔP)', fontsize=14, fontweight='bold')
ax_pipe.axis('off')

# Subplot 2: 배관 직경 vs 경제성(비용) 타당성 U-커브
ax_cost = plt.subplot(1, 2, 2)
ax_cost.set_title('파이프 구경 확장에 따른 경제성 마진 (Trade-off)', fontsize=14, fontweight='bold')
ax_cost.set_xlabel('배관 내경 D (m)')
ax_cost.set_ylabel('상대적 비용 규모 (Cost)')
ax_cost.grid(True, linestyle='--', alpha=0.6)

# UI 슬라이더 영역 설정
ax_v = plt.axes([0.15, 0.20, 0.7, 0.03])
ax_mu = plt.axes([0.15, 0.15, 0.7, 0.03])
ax_d = plt.axes([0.15, 0.10, 0.7, 0.03])

# 초기값 설정
s_v = Slider(ax_v, '타겟 유속 (m/s)', 0.5, 5.0, valinit=2.0)
s_mu = Slider(ax_mu, '유체 절대점도 (Pa.s)', 0.001, 0.1, valinit=0.01)
s_d = Slider(ax_d, '설계 배관 내경 D (m)', 0.02, 0.20, valinit=0.05)

# 공학 상수
L = 100.0 # 파이프 길이 100m
k1 = 0.02 # 펌프 마진 계수 (전력비 환산)
k2 = 1.0e6 # 파이프 설비 투자 마진 계수 (초대구경 파이프 자재/공간 설치비용)

# 기초 시각화 객체 생성 (배관)
d_init = s_d.val
pipe_outer = patches.Circle((0,0), radius=d_init/2, fill=False, color='black', lw=6)
ax_pipe.add_patch(pipe_outer)
fluid_inner = patches.Circle((0,0), radius=d_init/2 - 0.003, fill=True, color='skyblue', alpha=0.7)
ax_pipe.add_patch(fluid_inner)

friction_arrows = []
for _ in range(8):
    arrow = ax_pipe.annotate('', xy=(0,0), xytext=(0,0), arrowprops=dict(facecolor='red', edgecolor='red', width=3, headwidth=10))
    friction_arrows.append(arrow)

# 플롯 객체 생성
D_arr = np.linspace(0.02, 0.20, 100)
line_pump, = ax_cost.plot([], [], 'b--', label='펌프 가동비 (마찰 저항 비례)')
line_pipe, = ax_cost.plot([], [], 'g-.', label='파이프 설비 인프라 초기 비용')
line_total, = ax_cost.plot([], [], 'k-', lw=2, label='전체 통합 총비용 (Total Cost)')
pt_current, = ax_cost.plot([], [], 'ro', markersize=10, label='현재 조작 직경 라인')
opt_line = ax_cost.axvline(x=0.05, color='red', linestyle=':', alpha=0.7)

ax_cost.legend(loc='upper right')
ax_cost.set_xlim(0.02, 0.20)
ax_cost.set_ylim(0, 50000)

text_status = fig.text(0.5, 0.01, '', ha='center', fontsize=12, fontweight='bold', color='indigo')

def update(val=None):
    v = s_v.val
    mu = s_mu.val
    d_cur = s_d.val
    
    # 배관 애니메이션 크기 갱신
    pipe_outer.set_radius(d_cur/2)
    fluid_inner.set_radius(d_cur/2 - 0.003)
    
    # 하겐-푸아죄유 방정식 산출
    dP_cur = (32 * mu * L * v) / (d_cur**2)
    
    # 화살표(마찰 저항) 크기 매핑 - 내경 축소 시 압력 손실 제곱 폭주
    max_dP = (32 * mu * L * v) / (0.02**2)
    arrow_scale = np.clip(dP_cur / max_dP * (d_cur/2), 0.005, d_cur/2 - 0.003)
    
    angles = np.linspace(0, 2*np.pi, 8, endpoint=False)
    for i, angle in enumerate(angles):
        x_edge = (d_cur/2) * np.cos(angle)
        y_edge = (d_cur/2) * np.sin(angle)
        x_center = (d_cur/2 - arrow_scale) * np.cos(angle)
        y_center = (d_cur/2 - arrow_scale) * np.sin(angle)
        
        friction_arrows[i].xytext = (x_edge, y_edge)
        friction_arrows[i].xy = (x_center, y_center)
        
    # 경제성 U커브 갱신
    cost_pump_arr = k1 * (32 * mu * L * v) / (D_arr**2)
    cost_pipe_arr = k2 * (D_arr**2.5) # 체적이 커질수록 단가 2.5차 급증 수렴
    cost_total_arr = cost_pump_arr + cost_pipe_arr
    
    line_pump.set_data(D_arr, cost_pump_arr)
    line_pipe.set_data(D_arr, cost_pipe_arr)
    line_total.set_data(D_arr, cost_total_arr)
    
    # 마커 이동
    c_pump = k1 * (32 * mu * L * v) / (d_cur**2)
    c_pipe = k2 * (d_cur**2.5)
    c_tot = c_pump + c_pipe
    pt_current.set_data([d_cur], [c_tot])
    
    # 최적 비용 마일스톤
    min_idx = np.argmin(cost_total_arr)
    opt_d = D_arr[min_idx]
    opt_line.set_xdata([opt_d, opt_d])
    
    # Y-limit 스케일 조정계수
    ax_cost.set_ylim(0, np.percentile(cost_total_arr, 95) * 1.3)
    
    status_msg = (f"[실시간 피드백] 파이프 내경: {d_cur:.3f} m ➔ 현재 압력 손실액(ΔP): {dP_cur:,.0f} Pa\n"
                  f"💡 [최적 스키마 도출] 총비용 U-커브 최저점 마진: {opt_d:.3f} m\n"
                  f"▶ 토론 2 해설: 배관 저항을 줄이려 파이프를 무한정 비대하게 키우면 초기 인프라 설치비용(녹색 선) 폭탄을 맞습니다!")
    text_status.set_text(status_msg)
    
    fig.canvas.draw_idle()

s_v.on_changed(update)
s_mu.on_changed(update)
s_d.on_changed(update)

update()
plt.show()
