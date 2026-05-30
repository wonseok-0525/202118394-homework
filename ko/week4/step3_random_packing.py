import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import cdist

print("-" * 50)
print("🥑 Step 3: 가상 패킹 시뮬레이션 비교 (배열 적재 vs 무작위 적재)")
print("-" * 50)

# 1. 시뮬레이션 환경 및 농산물 규격 설정 
box_length = 40.0
box_width = 30.0
box_height = 15.0
box_vol = box_length * box_width * box_height

# 아보카도 평균 체적(205.4 cm³)을 토대로 완벽한 구형으로 가정했을 때의 등가 반경 계산
volume_single_cm3 = 205.4
radius = (3 * volume_single_cm3 / (4 * np.pi)) ** (1/3) # 약 3.66 cm

max_items = 45 # 기존 실습 목표 적재 개수

def generate_ordered_packing():
    """배열 적재 (Ordered Packing) - 직교 격자를 이용한 이상적인 규칙적 적재"""
    x_positions = np.linspace(radius, box_length - radius, 5)
    y_positions = np.linspace(radius, box_width - radius, 3)
    z_positions = np.linspace(radius, box_height - radius, 3)
    
    positions = []
    for z in z_positions:
        for y in y_positions:
            for x in x_positions:
                positions.append([x, y, z])
                if len(positions) == max_items:
                    return np.array(positions)
    return np.array(positions)

def generate_random_packing():
    """무작위 적재 (Random Packing) - 몬테카를로 난수 및 충돌 감지(Collision Detection) 알고리즘 적용"""
    positions = []
    max_attempts = 100000 # 최대 연산 시도 횟수
    attempts = 0
    
    np.random.seed(42) # 결과 재현성을 위한 고정 시드
    
    while len(positions) < max_items and attempts < max_attempts:
        # 상자 바깥으로 과일이 튀어나가지 않도록 중심점 난수 생성
        x = np.random.uniform(radius, box_length - radius)
        y = np.random.uniform(radius, box_width - radius)
        z = np.random.uniform(radius, box_height - radius)
        new_pos = np.array([x, y, z])
        
        if len(positions) == 0:
            positions.append(new_pos)
        else:
            # 기존 과일들 좌표와의 거리 계산 (scipy cdist 활용)
            # 두 과일의 중심 간 거리가 지름(2 * radius)보다 크면 충돌하지 않은 것으로 간주
            dists = cdist([new_pos], positions)[0]
            if np.all(dists >= 2 * radius):
                positions.append(new_pos)
        
        attempts += 1
        
    return np.array(positions), attempts

# 좌표 배열 연산 수행
ordered_pos = generate_ordered_packing()
random_pos, attempts_needed = generate_random_packing()

# 결과 출력
print(f"[배열 적재] 박스 내 안착 성공 개수: {len(ordered_pos)}/{max_items}")
print(f"[무작위 적재] 박스 내 안착 성공 개수: {len(random_pos)}/{max_items}")
print(f"   -> 무작위 연산 반복 횟수: {attempts_needed} 회\n")

if len(random_pos) < max_items:
    print("💡 [분석 포인트] 무작위 적재(Random Packing)에서는 불규칙한 공극 배열로 인해")
    print("   자투리 빈 공간이 퍼져버려, 동일 체적임에도 목표 개수를 100% 채울 수 없습니다.")
    print("   이러한 패킹 방식의 차이가 실무에서 '산물밀도(벌크 밀도)'의 급격한 저하를 일으키는 원인입니다.\n")

# 2. 3D 시각화 비교 패널
fig = plt.figure(figsize=(14, 6))

def plot_packing(ax, positions, title):
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.set_xlim([0, box_length])
    ax.set_ylim([0, box_width])
    ax.set_zlim([0, box_height])
    ax.set_xlabel("X (cm)")
    ax.set_ylabel("Y (cm)")
    ax.set_zlabel("Z (cm)")
    
    # 박스 테두리 와이어프레임 작도
    for s, e in [((0,0,0),(0,box_width,0)), ((0,0,0),(0,0,box_height)), ((0,box_width,0),(0,box_width,box_height)),
                 ((0,0,box_height),(0,box_width,box_height)), ((box_length,0,0),(box_length,box_width,0)),
                 ((box_length,0,0),(box_length,0,box_height)), ((box_length,box_width,0),(box_length,box_width,box_height)),
                 ((box_length,0,box_height),(box_length,box_width,box_height)),
                 ((0,0,0),(box_length,0,0)), ((0,box_width,0),(box_length,box_width,0)),
                 ((0,0,box_height),(box_length,0,box_height)), ((0,box_width,box_height),(box_length,box_width,box_height))]:
        ax.plot3D(*zip(s,e), color='black', linewidth=1, alpha=0.5)
        
    # 아보카도 구형 스캐터 플롯
    if len(positions) > 0:
        ax.scatter(positions[:, 0], positions[:, 1], positions[:, 2], 
                   s=1800, c='#4A90E2', alpha=0.8, edgecolors='#333333', linewidth=1.5)

# 좌측 패널: 배열 적재 (규칙적)
ax1 = fig.add_subplot(1, 2, 1, projection='3d')
plot_packing(ax1, ordered_pos, "Ordered Packing (Grid: 45 units)")

# 우측 패널: 무작위 적재 (비규칙적)
ax2 = fig.add_subplot(1, 2, 2, projection='3d')
plot_packing(ax2, random_pos, f"Random Packing (Fitted: {len(random_pos)} units)")

plt.tight_layout()
plt.show()
