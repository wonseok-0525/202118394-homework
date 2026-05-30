"""
[Step 2] 접촉 압력 분포 3D 시각화 (Contact Pressure Distribution 3D)
- 9주차 실습: 기계적 특성 I — 접촉 응력과 헤르츠 이론
- 헤르츠 접촉 원 내의 반타원형(Semi-ellipsoidal) 압력 프로파일 3D 렌더링
- 접촉 반경 변화에 따른 압력 분포 비교 멀티 서브플롯
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401
import matplotlib.font_manager as fm

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# ============================================================
# 1. 헤르츠 접촉 파라미터 설정
# ============================================================
# 사과(Fuji) - 평판 접촉 조건
R_fruit = 0.040       # 40 mm
E_fruit = 5.0e6       # 5 MPa
nu_fruit = 0.33
E_surface = 200e9     # 스테인리스 강
nu_surface = 0.30

# 복합 탄성 계수
E_star = 1.0 / ((1 - nu_fruit**2) / E_fruit + (1 - nu_surface**2) / E_surface)
R_star = R_fruit  # 구-평면 접촉

# ============================================================
# 2. 3가지 하중 조건에서 압력 분포 비교
# ============================================================
loads = [1.0, 5.0, 15.0]  # N
titles = ["F = 1.0 N\n(자중 ~100g)", "F = 5.0 N\n(적재 하중)", "F = 15.0 N\n(고하중)"]

fig = plt.figure(figsize=(18, 6))
fig.suptitle("Hertz Contact Pressure Distribution — Semi-ellipsoidal Profile",
             fontsize=14, fontweight="bold")

for idx, (F, title) in enumerate(zip(loads, titles)):
    # 접촉 반경 및 최대 압력 산출
    a = (3 * F * R_star / (4 * E_star)) ** (1/3)
    p0 = 3 * F / (2 * np.pi * a**2)
    
    # 그리드 생성
    margin = 1.5  # 접촉 원 외부 여백
    x = np.linspace(-a * margin, a * margin, 300)
    y = np.linspace(-a * margin, a * margin, 300)
    X, Y = np.meshgrid(x, y)
    R = np.sqrt(X**2 + Y**2)
    
    # 반타원형 압력 분포: p(r) = p0 * sqrt(1 - (r/a)^2)
    P = np.where(R <= a, p0 * np.sqrt(1 - (R / a)**2), 0)
    
    # 3D 서피스 플롯
    ax = fig.add_subplot(1, 3, idx + 1, projection="3d")
    surf = ax.plot_surface(X * 1e3, Y * 1e3, P / 1e3,
                            cmap="coolwarm", alpha=0.85,
                            edgecolor="none", antialiased=True)
    
    ax.set_xlabel("X (mm)", fontsize=10)
    ax.set_ylabel("Y (mm)", fontsize=10)
    ax.set_zlabel("Pressure (kPa)", fontsize=10)
    ax.set_title(f"{title}\na = {a*1e3:.2f} mm,  p_0 = {p0/1e3:.1f} kPa",
                 fontsize=11, pad=10)
    ax.view_init(elev=25, azim=-60)

plt.tight_layout()
plt.savefig("step2_result.png", dpi=150, bbox_inches="tight")
plt.show()

# ============================================================
# 3. 접촉 축(z축) 방향 응력 분포 — 깊이별 프로파일
# ============================================================
F_ref = 5.0  # 기준 하중 5 N
a_ref = (3 * F_ref * R_star / (4 * E_star)) ** (1/3)
p0_ref = 3 * F_ref / (2 * np.pi * a_ref**2)

z = np.linspace(0, 3 * a_ref, 500)
z_norm = z / a_ref

# 접촉 축 위의 응력 성분 (간략화된 해석적 근사)
sigma_z = -p0_ref / (1 + (z_norm)**2)
sigma_r = -p0_ref * (1 - z_norm * np.arctan(1 / (z_norm + 1e-10))) * 0.5
tau_max_profile = 0.5 * np.abs(sigma_z - sigma_r)

fig2, ax2 = plt.subplots(figsize=(8, 6))
ax2.plot(z_norm, -sigma_z / p0_ref, "b-", linewidth=2, label="σ_z / p_0 (수직 응력)")
ax2.plot(z_norm, -sigma_r / p0_ref, "g--", linewidth=2, label="σ_r / p_0 (반경 응력)")
ax2.plot(z_norm, tau_max_profile / p0_ref, "r-.", linewidth=2.5, label="τ_max / p_0 (최대 전단)")

# 최대 전단 응력 위치 표시
tau_peak_idx = np.argmax(tau_max_profile)
ax2.axvline(x=z_norm[tau_peak_idx], color="red", linestyle=":", alpha=0.5)
ax2.annotate(f"τ_max 극대\nz/a ≈ {z_norm[tau_peak_idx]:.2f}",
             xy=(z_norm[tau_peak_idx], tau_max_profile[tau_peak_idx] / p0_ref),
             xytext=(z_norm[tau_peak_idx] + 0.5, tau_max_profile[tau_peak_idx] / p0_ref + 0.05),
             fontsize=10, color="red",
             arrowprops=dict(arrowstyle="->", color="red"))

ax2.set_xlabel("Normalized Depth  z / a", fontsize=12)
ax2.set_ylabel("Normalized Stress  σ / p_0", fontsize=12)
ax2.set_title("Subsurface Stress Distribution along Contact Axis\n"
              f"(F = {F_ref:.0f} N, a = {a_ref*1e3:.2f} mm, p_0 = {p0_ref/1e3:.1f} kPa)",
              fontsize=12, fontweight="bold")
ax2.legend(fontsize=10)
ax2.grid(True, alpha=0.3)
ax2.set_xlim(0, 3)

plt.tight_layout()
plt.savefig("step2_subsurface.png", dpi=150, bbox_inches="tight")
plt.show()

print("=" * 55)
print("  🎨 3D 압력 분포: step2_result.png 저장 완료")
print("  📊 깊이별 응력 분포: step2_subsurface.png 저장 완료")
print("=" * 55)
