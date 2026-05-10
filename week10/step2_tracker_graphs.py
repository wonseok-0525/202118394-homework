import numpy as np
import matplotlib.pyplot as plt

# 한글 폰트 설정 (Windows: Malgun Gothic)
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# =====================================================================
# 1. Tracker 모의 가상 데이터 생성 
# (실제 Tracker로 뽑아낸 듯한 노이즈 포함 데이터 생성)
# =====================================================================
np.random.seed(42)
t_fall = 0.45      # 낙하 시간 (약 1m 높이 기준)
dt = 0.01          # Tracker 영상 프레임 시간 간격 (100fps)
t1 = np.arange(0, t_fall, dt)
g = 9.81
h0 = 1.0

# 1) 낙하 구간 (자유낙하)
y1 = h0 - 0.5 * g * t1**2

# 충돌 순간 매우 짧은 시간
t2_impact = np.array([t_fall, t_fall + dt])
y2_impact = np.array([0.0, 0.0])

# 2) 반발 구간 
# 반발계수(e) 약 0.5
e = 0.5
v_rebound = (g * t_fall) * e
t3_up = np.arange(t_fall + 2*dt, t_fall + 0.6, dt)
t_b = t3_up - (t_fall + dt)
y3 = v_rebound * t_b - 0.5 * g * t_b**2
# 바닥을 뚫고 들어가지 않게 처리
y3[y3 < 0] = 0

# 전체 시간 및 위치 결합
t = np.concatenate((t1, t2_impact, t3_up))
y = np.concatenate((y1, y2_impact, y3))

# 사람의 손떨림 등 Tracker 오차(노이즈) 약간 추가
noise = np.random.normal(0, 0.002, len(t))
y_noisy = y + noise
y_noisy[y_noisy < 0] = 0.0 # 위치가 음수가 되지 않도록 보정

# =====================================================================
# 2. 속도(v) 및 가속도(a) 계산 (수치 미분 중심차분법)
# =====================================================================
v = np.zeros_like(y_noisy)
a = np.zeros_like(y_noisy)

for i in range(1, len(v) - 1):
    v[i] = (y_noisy[i+1] - y_noisy[i-1]) / (2 * dt)
    
for i in range(1, len(a) - 1):
    a[i] = (v[i+1] - v[i-1]) / (2 * dt)

# 양 끝값 처리 처리
v[0], v[-1] = v[1], v[-2]
a[0], a[-1] = a[1], a[-2]

# 충돌 시점의 거대한 스파이크 가속도를 명확히 표현
# 실제 Tracker에서는 프레임 단위 한계로 충격량이 덜 측정될 수 있음
# 이 데이터에서는 충돌 프레임 위치에서 크게 음/양으로 튀는 걸 볼 수 있습니다.

# =====================================================================
# 3. 그래프 그리기 (위치-시간, 가속도-시간 2종)
# =====================================================================
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
fig.suptitle('Tracker 영상 분석 모의 결과 (낙하 궤적 및 가속도)', fontsize=16, fontweight='bold')

# 1) 위치-시간 그래프
ax1.plot(t, y_noisy, 'bo-', markersize=4, label='위치 (Position)')
ax1.set_ylabel('높이 (m)', fontsize=12)
ax1.set_title('1. 위치 - 시간 그래프 (y-t)', fontsize=14)
ax1.grid(True, linestyle='--', alpha=0.7)
ax1.axhline(0, color='r', linestyle='-', alpha=0.5, label='바닥')
ax1.legend(loc='upper right')

# 2) 가속도-시간 그래프
ax2.plot(t, a, 'go-', markersize=4, label='가속도 (Acceleration)')
ax2.set_xlabel('시간 (s)', fontsize=12)
ax2.set_ylabel('가속도 (m/s²)', fontsize=12)
ax2.set_title('2. 가속도 - 시간 그래프 (a-t)', fontsize=14)
ax2.grid(True, linestyle='--', alpha=0.7)
ax2.axhline(-g, color='orange', linestyle='--', linewidth=2, label='중력가속도 (-9.81m/s²)')
ax2.axhline(0, color='black', linewidth=1)
ax2.legend(loc='upper right')

# 레이아웃 조정 및 출력
plt.tight_layout()
plt.subplots_adjust(top=0.9)
plt.show()
