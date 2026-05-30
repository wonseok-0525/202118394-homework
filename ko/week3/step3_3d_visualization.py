"""
step3_3d_visualization.py — 이미지 기반 3D 회전체 재구성 및 시각화
================================================================
아보카도 이미지에서 추출한 프로파일을 3D 회전체로 재구성하고,
체적·표면적 결과를 함께 표시합니다.

실행: python step3_3d_visualization.py
의존성: pip install numpy scipy matplotlib opencv-python
"""
import numpy as np
from scipy.interpolate import CubicSpline
from scipy.integrate import simpson
import matplotlib.pyplot as plt
import matplotlib
import cv2
from mpl_toolkits.mplot3d import Axes3D

# --- 한글 폰트 설정 (Windows: Malgun Gothic) ---
matplotlib.rcParams['font.family'] = 'Malgun Gothic'
matplotlib.rcParams['axes.unicode_minus'] = False

# ============================================================
# Step 3-A: 아보카도 이미지에서 프로파일 데이터 로드
# ============================================================
from avocado_profile import extract_profile

data = extract_profile()
x_points = data['x_points']      # 스플라인 보간용 (~15개 이상)
r_points = data['r_points']
x_textbook = data['x_textbook']   # 교재 기준 6개 포인트 (표시용)
r_textbook = data['r_textbook']

source = '이미지 기반' if data['from_image'] else '교재 데이터'

cs = CubicSpline(x_points, r_points, bc_type='natural')
L = x_points[-1]

x_new = np.linspace(0, L, 100)
r_new = cs(x_new)
r_new = np.maximum(r_new, 0)

# ============================================================
# Step 3-B: 체적 및 표면적 계산
# ============================================================
areas = np.pi * (r_new ** 2)
volume = simpson(areas, x=x_new)

# 표면적: S = 2π ∫ r(x) × √(1 + (dr/dx)²) dx
dr_dx = cs(x_new, 1)  # 1차 도함수
surface_integrand = 2 * np.pi * r_new * np.sqrt(1 + dr_dx ** 2)
surface_area = simpson(surface_integrand, x=x_new)

print("=" * 50)
print(f"아보카도 3D 형상 재구성 결과 [{source}]")
print("=" * 50)
print(f"  추정 체적    : {volume:.2f} cm³")
print(f"  추정 표면적  : {surface_area:.2f} cm²")
print(f"  비표면적     : {surface_area / volume:.4f} cm⁻¹")
print("=" * 50)

# ============================================================
# Step 3-C: 3D 회전체 메시(Mesh) 생성
# ============================================================
theta = np.linspace(0, 2 * np.pi, 50)
X, THETA = np.meshgrid(x_new, theta)
R = cs(X)
R = np.maximum(R, 0)
Y = R * np.cos(THETA)
Z = R * np.sin(THETA)

# ============================================================
# Step 3-D: 시각화 (원본 이미지 + 3D + 2D 프로파일)
# ============================================================
if data['from_image'] and data['image'] is not None:
    fig = plt.figure(figsize=(18, 6))

    # [좌] 원본 이미지 + 윤곽선
    ax0 = fig.add_subplot(131)
    img_rgb = cv2.cvtColor(data['image'], cv2.COLOR_BGR2RGB)
    img_show = img_rgb.copy()
    cv2.drawContours(img_show, [data['contour']], -1, (255, 0, 0), 3)
    ax0.imshow(img_show)
    ax0.set_title('원본 이미지 (입력)', fontsize=12)
    ax0.axis('off')

    # [중] 3D 표면 플롯
    ax1 = fig.add_subplot(132, projection='3d')
    ax1.plot_surface(X, Y, Z, cmap='YlGn', alpha=0.8, edgecolor='none')
    ax1.set_xlabel('길이 x [cm]')
    ax1.set_ylabel('Y [cm]')
    ax1.set_zlabel('Z [cm]')
    ax1.set_title(f'3D 재구성\nV={volume:.1f} cm³', fontsize=11)
    ax1.set_box_aspect([2, 1, 1])

    # [우] 2D 단면 프로파일
    ax2 = fig.add_subplot(133)
    ax2.fill_between(x_new, r_new, -r_new, alpha=0.3, color='green',
                     label='회전체 단면')
    ax2.plot(x_new, r_new, 'g-', linewidth=2)
    ax2.plot(x_new, -r_new, 'g-', linewidth=2)
    ax2.plot(x_textbook, r_textbook, 'ro', markersize=8, label='측정 포인트')
    ax2.plot(x_textbook, -r_textbook, 'ro', markersize=8)
    for xp in x_textbook:
        ax2.axvline(x=xp, color='gray', linestyle='--', alpha=0.3)
    ax2.set_xlabel('길이 x [cm]')
    ax2.set_ylabel('반지름 r [cm]')
    ax2.set_title(f'2D 프로파일 (S={surface_area:.1f} cm²)', fontsize=11)
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    ax2.set_aspect('equal')

    plt.suptitle('Step 3: 이미지 → 프로파일 → 3D 회전체 재구성',
                 fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.show()

else:
    # --- 이미지 없이 기존 2패널 방식 ---
    fig = plt.figure(figsize=(14, 5))

    ax1 = fig.add_subplot(121, projection='3d')
    ax1.plot_surface(X, Y, Z, cmap='YlGn', alpha=0.8, edgecolor='none')
    ax1.set_xlabel('길이 x [cm]')
    ax1.set_ylabel('Y [cm]')
    ax1.set_zlabel('Z [cm]')
    ax1.set_title(f'3D 재구성 아보카도\nV = {volume:.1f} cm³, S = {surface_area:.1f} cm²')
    ax1.set_box_aspect([2, 1, 1])

    ax2 = fig.add_subplot(122)
    ax2.fill_between(x_new, r_new, -r_new, alpha=0.3, color='green',
                     label='회전체 단면')
    ax2.plot(x_new, r_new, 'g-', linewidth=2)
    ax2.plot(x_new, -r_new, 'g-', linewidth=2)
    ax2.plot(x_textbook, r_textbook, 'ro', markersize=8, label='측정 포인트')
    ax2.plot(x_textbook, -r_textbook, 'ro', markersize=8)
    for xp in x_textbook:
        ax2.axvline(x=xp, color='gray', linestyle='--', alpha=0.3)
    ax2.set_xlabel('길이 x [cm]')
    ax2.set_ylabel('반지름 r [cm]')
    ax2.set_title('2D 프로파일 단면')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    ax2.set_aspect('equal')

    plt.tight_layout()
    plt.show()
