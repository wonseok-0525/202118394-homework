"""
step1_interpolation.py — 아보카도 이미지 기반 프로파일 추출 및 큐빅 스플라인 보간
================================================================================
아보카도 레퍼런스 이미지(images/avocado_front_view.png)에서 OpenCV로 윤곽선을
자동 추출한 뒤, 큐빅 스플라인 보간으로 매끄러운 프로파일 곡선을 생성합니다.

실행: python step1_interpolation.py
의존성: pip install numpy scipy matplotlib opencv-python
"""
import numpy as np
from scipy.interpolate import CubicSpline
import matplotlib.pyplot as plt
import matplotlib
import cv2

# --- 한글 폰트 설정 (Windows: Malgun Gothic) ---
matplotlib.rcParams['font.family'] = 'Malgun Gothic'
matplotlib.rcParams['axes.unicode_minus'] = False

# ============================================================
# Step 1-A: 아보카도 이미지에서 프로파일 데이터 자동 추출
# ============================================================
from avocado_profile import extract_profile

data = extract_profile()
x_points = data['x_points']      # 스플라인 보간용 (~15개 이상)
r_points = data['r_points']
x_textbook = data['x_textbook']   # 교재 기준 6개 포인트 (표시용)
r_textbook = data['r_textbook']

print(f"\n{'='*50}")
print(f"추출된 프로파일 데이터 ({'이미지 기반' if data['from_image'] else '교재 데이터'})")
print(f"{'='*50}")
print(f"스플라인 보간용 포인트: {len(x_points)}개")
print(f"교재 기준 측정 포인트:")
for i, (x, r) in enumerate(zip(x_textbook, r_textbook)):
    print(f"  점 {i+1}: x = {x:6.2f} cm,  r = {r:6.3f} cm")

# ============================================================
# Step 1-B: 큐빅 스플라인 보간 (Cubic Spline Interpolation)
# ============================================================
cs = CubicSpline(x_points, r_points, bc_type='natural')
x_new = np.linspace(0, x_points[-1], 100)
r_new = cs(x_new)
r_new = np.maximum(r_new, 0)  # 음수 반지름 보정

# ============================================================
# Step 1-C: 시각화 — 원본 이미지 + 프로파일 비교
# ============================================================
if data['from_image'] and data['image'] is not None:
    # --- 이미지 처리 결과를 함께 표시 (3패널) ---
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    # [좌] 원본 이미지 + 검출된 윤곽선
    ax1 = axes[0]
    img_rgb = cv2.cvtColor(data['image'], cv2.COLOR_BGR2RGB)
    img_contour = img_rgb.copy()
    cv2.drawContours(img_contour, [data['contour']], -1, (255, 0, 0), 3)
    ax1.imshow(img_contour)
    ax1.set_title('원본 이미지 + 검출 윤곽선', fontsize=12)
    ax1.axis('off')

    # [중] 이진화 결과
    ax2 = axes[1]
    ax2.imshow(data['binary'], cmap='gray')
    ax2.set_title('Otsu 이진화 + 모폴로지 처리', fontsize=12)
    ax2.axis('off')

    # [우] 추출 프로파일 + 스플라인 보간
    ax3 = axes[2]
    # 조밀 프로파일 (이미지 추출)
    if data['x_dense'] is not None:
        ax3.fill_between(data['x_dense'], data['r_dense'], -data['r_dense'],
                         alpha=0.15, color='blue', label='이미지 추출 프로파일')
    # 보간 곡선
    ax3.fill_between(x_new, r_new, -r_new, alpha=0.3, color='green',
                     label='큐빅 스플라인 보간')
    ax3.plot(x_new, r_new, 'g-', linewidth=2)
    ax3.plot(x_new, -r_new, 'g-', linewidth=2)
    # 교재 기준 측정 포인트 (6개)
    ax3.plot(x_textbook, r_textbook, 'ro', markersize=8, label='교재 기준 측정 포인트')
    ax3.plot(x_textbook, -r_textbook, 'ro', markersize=8)
    # 스플라인 보간용 포인트
    ax3.plot(x_points, r_points, 'b^', markersize=5, alpha=0.5, label='보간용 포인트')
    ax3.set_xlabel('길이 방향 위치 x [cm]', fontsize=11)
    ax3.set_ylabel('반지름 r [cm]', fontsize=11)
    ax3.set_title('추출 프로파일 → 큐빅 스플라인', fontsize=12)
    ax3.legend(fontsize=9)
    ax3.grid(True, alpha=0.3)
    ax3.set_aspect('equal')

    plt.suptitle('Step 1: 아보카도 이미지 → 프로파일 추출 → 스플라인 보간',
                 fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.show()

else:
    # --- 이미지 없이 교재 데이터만 표시 (기존 방식) ---
    plt.figure(figsize=(10, 5))
    plt.fill_between(x_new, r_new, -r_new, alpha=0.3, color='green',
                     label='보간 단면 (Interpolated Cross-section)')
    plt.plot(x_new, r_new, 'g-', linewidth=2)
    plt.plot(x_new, -r_new, 'g-', linewidth=2)
    plt.plot(x_textbook, r_textbook, 'ro', markersize=8, label='측정 데이터 (Measured Data)')
    plt.plot(x_textbook, -r_textbook, 'ro', markersize=8)
    plt.xlabel('길이 방향 위치 x [cm]', fontsize=12)
    plt.ylabel('반지름 r [cm]', fontsize=12)
    plt.title('Step 1: 아보카도 프로파일 - 큐빅 스플라인 보간', fontsize=14)
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.axis('equal')
    plt.tight_layout()
    plt.show()

# --- 결과 요약 출력 ---
print(f"\n스플라인 보간용 포인트 수: {len(x_points)}개")
print(f"교재 기준 측정 포인트 수: {len(x_textbook)}개")
print(f"보간 후 포인트 수: {len(x_new)}개")
print(f"아보카도 전체 길이: {x_points[-1]:.2f} cm")
print(f"최대 반지름: {r_points.max():.3f} cm")
