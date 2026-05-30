import numpy as np
import matplotlib.pyplot as plt

# 백엔드 Matplotlib 윈도우 UI 대응 한글 폰트 매핑 인코딩 삽입
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False # 좌표 마이너스(-) 기호 블록 붕괴 제어

print("==================================================")
print(" 🍏 5주차 실습: 맑은 사과즙 이송 파이프라인 시뮬레이터 ")
print("==================================================\n")

# [파트 1] 온도-점도 데이터 배열 구축
# 1. 온도 범위 설정: 10도 ~ 80도 (1도 단위 스텝)
temps_C = np.arange(10, 81, 1)

# 2. 섭씨 온도를 켈빈(절대온도)으로 치환
temps_K = temps_C + 273.15

# 3. 보편 기체 상수 및 아레니우스 모델 파라미터 세팅
R_const = 8.314  # 범용 기체 상수
mu_0 = 0.0001    # 베이스 점도 상수
E_a = 18000      # 활성화 에너지 지수

# 4. 아레니우스 방정식에 따른 점도(Viscosity) 배열 계산
viscosity_array = mu_0 * np.exp(E_a / (R_const * temps_K))

print("[STEP 1] 아레니우스 점도 스크래치 연산 완료")
print(f" -> 10도일 때의 점도: {viscosity_array[0]:.5f} Pa·s")
print(f" -> 80도일 때의 점도: {viscosity_array[-1]:.5f} Pa·s\n")

# [파트 2] 배관 마찰 마진 연산 로직 (하겐-푸아죄유 방정식 활용)
# 1. 배관 기하학 상수 및 타겟 유속 지정
pipe_L = 100.0   # 배관 길이 (m)
pipe_D = 0.05    # 배관 내경 (m)
velocity = 2.0   # 유체의 이동 속도 (m/s)

# 2. 마찰 압력 강하(Pressure Drop) 배열 계산
delta_P_array = (32 * viscosity_array * pipe_L * velocity) / (pipe_D ** 2)

# 3. 유체의 체적 유량(Volumetric Flow Rate) 산출 및 모터 효율 세팅
pump_efficiency = 0.7  # 펌프 효율 (70%)
vol_flow = (np.pi * (pipe_D / 2) ** 2) * velocity

print("[STEP 2] 파이프라인 유동 저항 및 압력 강하 연산 완료")
print(f" -> 체적 유량: {vol_flow:.5f} m^3/s")
print(f" -> 10도일 때의 100m 구간 압력 마찰 강하: {delta_P_array[0]:.2f} Pa\n")

# [파트 3] 펌핑 동력 vs 가열 전력 비용 밸런스 시뮬레이션
# 1. 펌프 소모 전력(W) 계산 및 연간 비용(원) 환산
pump_power_W = (vol_flow * delta_P_array) / pump_efficiency
run_hours = 1000        # 연간 구동 시간 (1000시간)
elec_cost_kw = 120      # 전력 단가 (원/kWh)

cost_pump_array = (pump_power_W / 1000) * run_hours * elec_cost_kw

# 2. 초기 온도 대비 목표 온도 도달을 위한 히팅 에너지(보일러) 스레드 연산
init_temp = 10.0        # 대기 상태 초기 온도 (10도)
heat_cp = 4.18          # 사과즙(수분 베이스) 비열 근사치 (kJ/kg·K)
heat_rate = vol_flow * 1000  # 물의 밀도(1000kg/m^3)를 가정한 질량 유량(kg/s)

# 3. 가열 전력 코스트 비용 배열 환산 
# heat_kw_array는 kJ/s 즉, kW 단위
heat_kw_array = heat_rate * heat_cp * (temps_C - init_temp) 
heat_cost_kw = 40       # 가열(스팀) 단가 (원/MJ 혹은 근사 전기열 환산)

cost_heat_array = heat_kw_array * run_hours * heat_cost_kw

# 4. 최종 통합 코스트(물류 에너지 비용 + 가열 비용) 합성
cost_total_array = cost_pump_array + cost_heat_array

print("[STEP 3] 에너지 트레이드오프(Trade-off) 비용 산출 완료\n")

# [파트 4] UI 시각 데이터 랜더링 통합 분석
# 1. np.argmin()을 이용한 총비용 최저점(최적 온도) 색출
min_idx = np.argmin(cost_total_array)
optimal_temp = temps_C[min_idx]

print("==================================================")
print(f" 🎯 시뮬레이션 결과: 에너지 코스트 최저점 온도는 [{optimal_temp}℃] 입니다.")
print("==================================================\n")

# 2. 다중 서브플롯 인포그래픽 출력 (1x2 형태)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# [서브플롯 1] 점도 및 마찰 압력 강하 곡선 (이중 Y축)
color1 = '#0056b3'
ax1.set_xlabel('파이프라인 이송 온도 (℃)', fontsize=12)
ax1.set_ylabel('절대 점도 (Pa·s)', color=color1, fontsize=12)
ax1.plot(temps_C, viscosity_array, color=color1, linewidth=2, label='점도 하강 곡선')
ax1.tick_params(axis='y', labelcolor=color1)
ax1.grid(True, linestyle=':', alpha=0.5)

ax1_twin = ax1.twinx()  # 이중 Y축 공유
color2 = '#d9534f'
ax1_twin.set_ylabel('파이프 마찰 압력 강하 (Pa)', color=color2, fontsize=12)
ax1_twin.plot(temps_C, delta_P_array, color=color2, linestyle='--', linewidth=2, label='압력 강하 곡선')
ax1_twin.tick_params(axis='y', labelcolor=color2)

ax1.set_title('온도 상승에 따른 점도 및 마찰 저항 변화율', fontsize=14, fontweight='bold')
lines_1, labels_1 = ax1.get_legend_handles_labels()
lines_2, labels_2 = ax1_twin.get_legend_handles_labels()
ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper right', fontsize=10)

# [서브플롯 2] 에너지 코스트 트레이드오프 마진 분석
ax2.plot(temps_C, cost_pump_array, label='모터 펌프 이송 비용', linestyle='--', color='blue', alpha=0.7)
ax2.plot(temps_C, cost_heat_array, label='보일러 예열 가열 비용', linestyle='-.', color='orange', alpha=0.7)
ax2.plot(temps_C, cost_total_array, label='통합 에너지 코스트 (Total)', linewidth=2.5, color='green')

# 최적 온도를 가리키는 수직 가이드라인 및 포인트 마커 추가
ax2.axvline(x=optimal_temp, color='red', alpha=0.5, label=f'최적 이송 온도: {optimal_temp}℃')
ax2.plot(optimal_temp, cost_total_array[min_idx], 'ro', markersize=8) # 최저점 마킹

ax2.set_title('펌핑-가열 이중 코스트 트레이드오프 분석', fontsize=14, fontweight='bold')
ax2.set_xlabel('파이프라인 이송 온도 (℃)', fontsize=12)
ax2.set_ylabel('에너지 단가 총비용 (원)', fontsize=12)
ax2.legend(loc='upper right', fontsize=10)
ax2.grid(True, linestyle=':', alpha=0.7)

# 화면 레이아웃 및 렌더링 릴리즈
plt.tight_layout()
plt.show()
