"""
step2_volume.py — 이미지 기반 프로파일을 이용한 수치 적분 체적 추정
================================================================
step1에서 추출한 아보카도 프로파일 데이터를 큐빅 스플라인으로 보간하고,
Simpson 공식 및 사다리꼴 공식으로 회전체의 체적을 산출합니다.

실행: python step2_volume.py
의존성: pip install numpy scipy opencv-python
"""
import numpy as np
from scipy.interpolate import CubicSpline
from scipy.integrate import simpson, trapezoid

# ============================================================
# Step 2-A: 아보카도 이미지에서 프로파일 데이터 로드
# ============================================================
from avocado_profile import extract_profile

data = extract_profile()
x_points = data['x_points']      # 스플라인 보간용 (~15개 이상)
r_points = data['r_points']
x_textbook = data['x_textbook']   # 교재 기준 6개 포인트 (표시용)
r_textbook = data['r_textbook']

source = '이미지 기반' if data['from_image'] else '교재 데이터'
print(f"[데이터 소스] {source}")

cs = CubicSpline(x_points, r_points, bc_type='natural')

# ============================================================
# Step 2-B: 분할 수(n)에 따른 적분 정밀도 비교
# ============================================================
print("\n" + "=" * 60)
print(f"분할 수(n)에 따른 체적 추정값 비교 [{source}]")
print("=" * 60)
print(f"{'분할 수(n)':>10} | {'Simpson [cm³]':>15} | {'Trapezoidal [cm³]':>18} | {'차이 [cm³]':>12}")
print("-" * 60)

L = x_points[-1]  # 아보카도 전체 길이

for n in [10, 20, 50, 100, 500, 1000]:
    x_new = np.linspace(0, L, n)
    r_new = cs(x_new)
    r_new = np.maximum(r_new, 0)

    # 단면적 계산: A(x) = π × r(x)²
    areas = np.pi * (r_new ** 2)

    # 심슨 공식 (Simpson's Rule) — 포물선 근사
    vol_simpson = simpson(areas, x=x_new)

    # 사다리꼴 공식 (Trapezoidal Rule) — 직선 근사
    vol_trapezoid = trapezoid(areas, x=x_new)

    diff = abs(vol_simpson - vol_trapezoid)
    print(f"{n:>10} | {vol_simpson:>15.4f} | {vol_trapezoid:>18.4f} | {diff:>12.6f}")

# ============================================================
# Step 2-C: 최종 체적 산출 (n=100 기준)
# ============================================================
print("\n" + "=" * 60)
print(f"최종 체적 추정 결과 (n = 100) [{source}]")
print("=" * 60)

x_final = np.linspace(0, L, 100)
r_final = cs(x_final)
r_final = np.maximum(r_final, 0)
areas_final = np.pi * (r_final ** 2)

vol_simpson_final = simpson(areas_final, x=x_final)
vol_trapezoid_final = trapezoid(areas_final, x=x_final)

# 교재 예제 3-3의 수동 분할 계산 결과 (참고값)
vol_manual = 334.1  # cm³

print(f"  Simpson's Rule   : {vol_simpson_final:.4f} cm³")
print(f"  Trapezoidal Rule : {vol_trapezoid_final:.4f} cm³")
print(f"  교재 수동 계산값  : {vol_manual:.1f} cm³ (5개 구간 분할)")

if vol_manual > 0:
    err_simpson = abs(vol_simpson_final - vol_manual) / vol_manual * 100
    err_trap = abs(vol_trapezoid_final - vol_manual) / vol_manual * 100
    print(f"\n  Simpson  vs 수동계산 차이: {err_simpson:.2f}%")
    print(f"  Trapezoid vs 수동계산 차이: {err_trap:.2f}%")

if data['from_image']:
    print(f"\n[참고] 이미지에서 추출한 프로파일은 실제 시료의 형상에 따라")
    print(f"       교재 수동 계산값과 차이가 있을 수 있습니다.")

print("\n[고찰] 분할 수가 증가할수록 Simpson과 Trapezoidal의 차이가")
print("       0에 수렴하며, 두 방법 모두 안정적인 체적값으로 수렴합니다.")
print("       Simpson 공식은 2차 포물선 근사를 사용하므로 동일한 분할 수에서")
print("       Trapezoidal보다 높은 정확도를 보입니다.")
