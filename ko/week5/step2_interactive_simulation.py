import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# 백엔드 Matplotlib 윈도우 UI 대응 한글 폰트 세팅
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False 

print("==================================================")
print(" 🍏 5주차 실습 Step 2: 실시간 인터랙티브 시뮬레이터 ")
print("==================================================\n")
print("UI 하단의 슬라이더 바를 조절하여 마찰 파라미터 최적화 곡선을 관찰하세요!")

# 1. 시뮬레이션 환경 변수 및 고정 상수 초기화
R_const = 8.314
pipe_L_init = 100.0
pump_efficiency = 0.7
run_hours = 1000
init_temp = 10.0
heat_cp = 4.18
temps_C = np.arange(10, 81, 1)
temps_K = temps_C + 273.15

# 슬라이더 초기값 세팅
pipe_D_init = 0.05
velocity_init = 2.0
mu_0_init = 0.0001
E_a_init = 18000
elec_cost_kw_init = 120
heat_cost_kw_init = 40

# 2. 비용 및 저항 계산 핵심 함수 정의
def calc_costs(pipe_D, velocity, mu_0, E_a, elec_cost, heat_cost):
    # 아레니우스 및 하겐-푸아죄유 수식 연계
    viscosity = mu_0 * np.exp(E_a / (R_const * temps_K))
    delta_P = (32 * viscosity * pipe_L_init * velocity) / (pipe_D ** 2)
    vol_flow = (np.pi * (pipe_D / 2) ** 2) * velocity
    
    pump_power_W = (vol_flow * delta_P) / pump_efficiency
    cost_pump = (pump_power_W / 1000) * run_hours * elec_cost
    
    heat_rate = vol_flow * 1000
    heat_kw = heat_rate * heat_cp * (temps_C - init_temp)
    cost_heat = heat_kw * run_hours * heat_cost
    
    cost_total = cost_pump + cost_heat
    return cost_pump, cost_heat, cost_total

# 3. 메인 Matplotlib Figure 및 축 생성
fig, ax = plt.subplots(figsize=(10, 8))
plt.subplots_adjust(bottom=0.5) # 슬라이더를 배치하기 위해 하단 공간을 비움

# 초기 데이터 시각화 매핑
cp_init, ch_init, ct_init = calc_costs(pipe_D_init, velocity_init, mu_0_init, E_a_init, elec_cost_kw_init, heat_cost_kw_init)

l_pump, = ax.plot(temps_C, cp_init, label='모터 펌프 이송 비용', linestyle='--', color='blue', alpha=0.7)
l_heat, = ax.plot(temps_C, ch_init, label='보일러 예열 가열 비용', linestyle='-.', color='orange', alpha=0.7)
l_total, = ax.plot(temps_C, ct_init, label='통합 에너지 코스트 (Total)', linewidth=2.5, color='green')

opt_idx = np.argmin(ct_init)
opt_temp = temps_C[opt_idx]
opt_line = ax.axvline(x=opt_temp, color='red', alpha=0.5, label=f'최적 이송 온도: {opt_temp}℃')

ax.set_title('동적 파라미터 조절 기반 펌프-예열 트레이드오프 실시간 분석', fontsize=14, fontweight='bold')
ax.set_xlabel('파이프라인 이송 온도 (℃)', fontsize=12)
ax.set_ylabel('연간 단위 총 에너지 운영 비용 (원)', fontsize=12)
ax.legend(loc='upper right')
ax.grid(True, linestyle=':', alpha=0.7)

# 4. 동적 제어용 슬라이더 UI 축 생성
axcolor = 'whitesmoke'
ax_D  = plt.axes([0.20, 0.40, 0.65, 0.03], facecolor=axcolor)
ax_v  = plt.axes([0.20, 0.35, 0.65, 0.03], facecolor=axcolor)
ax_mu = plt.axes([0.20, 0.30, 0.65, 0.03], facecolor=axcolor)
ax_Ea = plt.axes([0.20, 0.25, 0.65, 0.03], facecolor=axcolor)
ax_el = plt.axes([0.20, 0.20, 0.65, 0.03], facecolor=axcolor)
ax_ht = plt.axes([0.20, 0.15, 0.65, 0.03], facecolor=axcolor)

# 슬라이더 컴포넌트 장착
s_D  = Slider(ax_D,  '배관 내경(m)', 0.01, 0.20, valinit=pipe_D_init, valstep=0.01)
s_v  = Slider(ax_v,  '타겟 유속(m/s)', 0.5, 10.0, valinit=velocity_init, valstep=0.1)
s_mu = Slider(ax_mu, '초기 점도(mu_0)', 0.00001, 0.002, valinit=mu_0_init, valfmt='%1.5f')
s_Ea = Slider(ax_Ea, '활성화 에너지', 10000, 30000, valinit=E_a_init, valstep=500)
s_el = Slider(ax_el, '전기 단가(원/kWh)', 50, 300, valinit=elec_cost_kw_init, valstep=10)
s_ht = Slider(ax_ht, '보일러 단가(원/MJ)', 10, 150, valinit=heat_cost_kw_init, valstep=5)

# 5. 슬라이더 인터랙션 콜백 데이터 주입 함수
def update(val):
    # 슬라이더 강제 업데이트
    cp, ch, ct = calc_costs(s_D.val, s_v.val, s_mu.val, s_Ea.val, s_el.val, s_ht.val)
    
    # 그래프 좌표 재설정
    l_pump.set_ydata(cp)
    l_heat.set_ydata(ch)
    l_total.set_ydata(ct)
    
    # 동적 스케일 리밋 재정의 (애니메이션 갱신)
    ax.relim()
    ax.autoscale_view()
    
    # 최적 온도 라인 위치 재정의
    idx = np.argmin(ct)
    new_opt_temp = temps_C[idx]
    opt_line.set_xdata([new_opt_temp, new_opt_temp])
    opt_line.set_label(f'최적 이송 온도: {new_opt_temp}℃')
    
    ax.legend(loc='upper right')
    fig.canvas.draw_idle()

# 이벤트 트리거 바인딩 설정
s_D.on_changed(update)
s_v.on_changed(update)
s_mu.on_changed(update)
s_Ea.on_changed(update)
s_el.on_changed(update)
s_ht.on_changed(update)

# 화면 송출
plt.show()
