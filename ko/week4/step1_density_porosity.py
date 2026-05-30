# -*- coding: utf-8 -*-
"""
생물자원가공공학 및 실습 - 4주차 실습
주제: 곡물 및 과채류의 밀도와 공극률 계산 및 시각화 (Density & Porosity)

본 스크립트는 3주차 실습에서 도출된 아보카도 체적(Volume) 데이터와
가상의 질량(Mass) 및 포장 박스 데이터를 활용하여 
'진밀도(겉보기밀도)', '산물밀도(Bulk Density)', '공극률(Porosity)'을 계산하고
결과를 시각화하는 전체 파이프라인을 다룹니다.
"""

import numpy as np
import matplotlib.pyplot as plt
from itertools import product, combinations
from scipy.spatial.distance import cdist  # 추가: 공간 거리 연산 모듈

# 한글 폰트 설정 (Windows 환경)
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# =====================================================================
# [Step 1] 개별 대상(아보카도 1개)의 부피와 질량 (진밀도/겉보기밀도 계산)
# =====================================================================
# 3주차 실습에서 도출된 개별 아보카도 체적 (Simpson 적분 기준 약 205.4 cm^3)
volume_single_cm3 = 205.4
# 가상의 아보카도 개별 질량 측정값 (저울 측정 가정, 215.0 g)
mass_single_g = 215.0

# 개별 객체의 밀도 (Particle Density) 계산
# 생물자원 특성상 기공이 없다고 가정하면 진밀도 ≒ 겉보기밀도로 간주 가능
density_particle = mass_single_g / volume_single_cm3

print(f"{'='*50}")
print(f"[Step 1] 개별 객체 밀도 (Particle Density)")
print(f"{'='*50}")
print(f" - 단일 개체 체적 : {volume_single_cm3:>8.2f} cm^3")
print(f" - 단일 개체 질량 : {mass_single_g:>8.2f} g")
print(f" -> 산출된 개별 밀도: {density_particle:>8.3f} g/cm^3")
print(f"    (물 밀도 1.0보다 크므로 침강 현상 발생 예상)")

# =====================================================================
# [Step 2] 포장 박스에 적재된 전체 대상(산물)의 밀도 (Bulk Density 계산)
# =====================================================================
# 가상의 표준 플라스틱 물류 상자 규격 (가로 40cm * 세로 30cm * 높이 15cm)
box_volume_cm3 = 40.0 * 30.0 * 15.0  # 18,000 cm^3
# 해당 박스에 들어가는 아보카도의 총 적재 개수
avocado_count = 45

# 적재된 전체 질량 (단일 질량 * 적재 개수)
mass_total_g = mass_single_g * avocado_count

# 박스 내 전체 부피를 기준으로 한 산물밀도(Bulk Density)
density_bulk = mass_total_g / box_volume_cm3

print(f"\n{'='*50}")
print(f"[Step 2] 포장된 산물 밀도 (Bulk Density)")
print(f"{'='*50}")
print(f" - 포장 상자 총 체적: {box_volume_cm3:>8.2f} cm^3")
print(f" - 적재된 객체 총수 : {avocado_count:>8} 개")
print(f" - 박스 내 전체 질량: {mass_total_g:>8.2f} g")
print(f" -> 산출된 산물 밀도: {density_bulk:>8.3f} g/cm^3")

# =====================================================================
# [Step 3] 공극률 (Porosity) 교차 검증 계산
# =====================================================================
# 방법 A: 밀도 비율 기반의 공극률 계산 공식 이용
# Porosity = 1 - (Bulk Density / Particle Density)
porosity_density_based = (1 - (density_bulk / density_particle)) * 100

# 방법 B: 물리적 부피 차감을 이용한 정석 계산
# 실제 허공(Void) 부피 = 박스 전체 부피 - (개별 객체 부피 * 총 개수)
void_volume = box_volume_cm3 - (volume_single_cm3 * avocado_count)
porosity_volume_based = (void_volume / box_volume_cm3) * 100

print(f"\n{'='*50}")
print(f"[Step 3] 공극률 (Porosity) 도출 및 상호 검증")
print(f"{'='*50}")
print(f" A. 밀도 비율 연산 공극률 : {porosity_density_based:>6.2f} %")
print(f" B. 체적 차감 연산 공극률 : {porosity_volume_based:>6.2f} %")
if abs(porosity_density_based - porosity_volume_based) < 1e-5:
    print(f" -> [검증 성공] 수식이 완벽히 일치합니다.")
else:
    print(f" -> [검증 실패] 오차가 발생했습니다.")

# =====================================================================
# [Step 4] 시각화 (3D Packing / Bar / Pie Chart)
# =====================================================================
fig = plt.figure(figsize=(18, 6))

# ---- (A) 좌측: 3D 가상 패킹 시뮬레이션 (공간 직관화) ----
ax1 = fig.add_subplot(131, projection='3d')

# 40x30x15 박스 외곽선(Wireframe) 그리기
r = [0, 40]
for s, e in combinations(np.array(list(product(r, [0, 30], [0, 15]))), 2):
    if np.sum(np.abs(s-e)) in [40, 30, 15]:
        ax1.plot3D(*zip(s, e), color="black", linestyle='--', alpha=0.3)

# 45개의 아보카도를 가상격자(5x3x3)에 배치
x_centers = np.linspace(4, 36, 5)
y_centers = np.linspace(5, 25, 3)
z_centers = np.linspace(2.5, 12.5, 3)
X, Y, Z = np.meshgrid(x_centers, y_centers, z_centers)

# 공극 포인트 생성: 더 세밀한 격자
vx = np.linspace(0, 40, 20)
vy = np.linspace(0, 30, 15)
vz = np.linspace(0, 15, 8)
VX, VY, VZ = np.meshgrid(vx, vy, vz)

void_pts = np.vstack((VX.flatten(), VY.flatten(), VZ.flatten())).T
center_pts = np.vstack((X.flatten(), Y.flatten(), Z.flatten())).T

# 객체(아보카도) 중심으로부터 일정 반경(R) 이상 떨어진 점들만 추출
# 아보카도 체적 약 205cm^3 -> 구 환산 시 반경 약 3.66cm
R_avocado = 3.6 
distances = cdist(void_pts, center_pts)
is_void = np.min(distances, axis=1) > R_avocado

# 빈 공간(공극)을 붉은색 반투명 점으로 시각화 (유체나 공기를 붉은색 영역으로 표현)
ax1.scatter(void_pts[is_void, 0], void_pts[is_void, 1], void_pts[is_void, 2], 
            s=15, c='red', alpha=0.3, label='Void (공극)')

# 아보카도들을 3D Scatter로 표시 (크기, 색상 조정)
ax1.scatter(X, Y, Z, s=600, c='#8BC34A', alpha=1.0, edgecolors='#33691E', label='Avocado')

ax1.set_title('Step 4-a: 3D 가상 패킹 (공극 직접 확인)', fontsize=14, pad=15)
ax1.set_xlabel('길이 (40cm)')
ax1.set_ylabel('너비 (30cm)')
ax1.set_zlabel('높이 (15cm)')
ax1.set_box_aspect((40, 30, 15))  # 박스 비율 보정
ax1.legend(loc='upper right', fontsize=10)

# ---- (B) 중앙: 밀도 비교 막대 차트 (Bar Chart) ----
ax2 = fig.add_subplot(132)
labels = ['파티클 개별 밀도\n(Particle)', '벌크 산물 밀도\n(Bulk)']
values = [density_particle, density_bulk]
colors = ['#0056b3', '#80bfff']

bars = ax2.bar(labels, values, color=colors, width=0.5, edgecolor='black')
ax2.set_ylabel('밀도 [g/cm³]', fontsize=12)
ax2.set_title('Step 4-b: 개별 밀도 vs 산물 밀도 갭 분석', fontsize=14, pad=15)
ax2.set_ylim(0, max(values) * 1.3)
ax2.grid(axis='y', linestyle='--', alpha=0.5)

# 수치 텍스트 표시
for bar in bars:
    y_val = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2, y_val + 0.03, 
             f'{y_val:.3f}', ha='center', va='bottom', fontweight='bold', fontsize=11)

# ---- (C) 우측: 포장 박스 내 체적 파이 차트 (Pie Chart) ----
ax3 = fig.add_subplot(133)
pie_labels = ['아보카도 체적\n(점유 공간)', '빈 공기층\n(공극률 산출치)']
pie_sizes = [100 - porosity_density_based, porosity_density_based]
pie_colors = ['#8BC34A', '#e6f0ff']
explode = (0.05, 0) # 아보카도 점유 파트를 강조하기 위해 분리

ax3.pie(pie_sizes, explode=explode, labels=pie_labels, colors=pie_colors,
        autopct='%1.1f%%', shadow=False, startangle=140, 
        textprops={'fontsize': 13, 'fontweight': 'bold'},
        wedgeprops={'edgecolor': 'black', 'linewidth': 1})
ax3.set_title(f'Step 4-c: 점유율 및 공극률 ({avocado_count}개 적재 시)', fontsize=14, pad=15)

# 레이아웃 간섭 방지 처리 및 화면 표시
plt.tight_layout()
plt.show()
