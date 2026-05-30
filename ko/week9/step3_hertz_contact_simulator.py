"""
[Step 3] 인터랙티브 접촉 응력 시뮬레이터 (Interactive Hertz Contact Simulator)
- 9주차 실습: 기계적 특성 I — 접촉 응력과 헤르츠 이론
- 슬라이더 UI로 과일 반경, 영률, 포아송 비 실시간 조절
- 접촉면 재질 라디오 버튼 전환
- 좌: F-δ 곡선(하중-침투) + 우: 접촉 압력 분포 듀얼 플로팅
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, RadioButtons
import matplotlib.font_manager as fm

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# ============================================================
# 1. 초기 파라미터
# ============================================================
R_init = 40.0       # 과일 반경 (mm)
E_init = 5.0        # 과일 영률 (MPa)
nu_init = 0.33      # 포아송 비
F_max = 20.0        # 최대 하중 (N)

# 접촉면 재질 DB (스테인리스, 경질 고무, 연질 실리콘, 에어 쿠션)
surface_db = {
    "Steel":    {"E": 200e9,  "nu": 0.30, "label": "스테인리스 강"},
    "Rubber":   {"E": 30e6,   "nu": 0.45, "label": "경질 고무"},
    "Silicone": {"E": 2e6,    "nu": 0.48, "label": "연질 실리콘"},
    "Air":      {"E": 0.05e6, "nu": 0.49, "label": "에어 쿠션"},
}
current_surface = "Steel"

BIO_YIELD = 300e3  # Bio-yield Stress (Pa)

# ============================================================
# 2. 헤르츠 계산 함수
# ============================================================
def calc_E_star(E1, nu1, E2, nu2):
    return 1.0 / ((1 - nu1**2) / E1 + (1 - nu2**2) / E2)

def hertz_Fd(F_arr, R_star, E_star):
    """하중 배열 → 침투 깊이 배열"""
    a_arr = (3 * F_arr * R_star / (4 * E_star)) ** (1/3)
    delta_arr = a_arr**2 / R_star
    sigma_arr = 3 * F_arr / (2 * np.pi * a_arr**2)
    return delta_arr, sigma_arr, a_arr

# ============================================================
# 3. 그래프 초기 설정
# ============================================================
fig, (ax_fd, ax_pressure) = plt.subplots(1, 2, figsize=(15, 6))
fig.subplots_adjust(left=0.08, right=0.70, bottom=0.35, top=0.88)
fig.suptitle("Interactive Hertz Contact Simulator", fontsize=14, fontweight="bold")

F_arr = np.linspace(0.01, F_max, 300)

# 초기 계산
R_m = R_init * 1e-3
E_fruit_Pa = E_init * 1e6
surf = surface_db[current_surface]
E_star = calc_E_star(E_fruit_Pa, nu_init, surf["E"], surf["nu"])
R_star = R_m

delta_arr, sigma_arr, a_arr = hertz_Fd(F_arr, R_star, E_star)

# 좌측: F-δ 곡선
line_fd, = ax_fd.plot(delta_arr * 1e3, F_arr, "b-", linewidth=2)
ax_fd.set_xlabel("Penetration Depth δ (mm)", fontsize=11)
ax_fd.set_ylabel("Contact Force F (N)", fontsize=11)
ax_fd.set_title("Force - Displacement Curve", fontsize=12)
ax_fd.grid(True, alpha=0.3)

# 우측: 접촉 압력 분포 (단면)
F_ref = 5.0
a_ref = (3 * F_ref * R_star / (4 * E_star)) ** (1/3)
p0_ref = 3 * F_ref / (2 * np.pi * a_ref**2)
r_arr = np.linspace(-a_ref * 1.5, a_ref * 1.5, 500)
p_arr = np.where(np.abs(r_arr) <= a_ref, 
                  p0_ref * np.sqrt(1 - (r_arr / a_ref)**2), 0)

line_p, = ax_pressure.plot(r_arr * 1e3, p_arr / 1e3, "r-", linewidth=2)
line_bio = ax_pressure.axhline(y=BIO_YIELD / 1e3, color="gray", linestyle="--", 
                                linewidth=1.5, label=f"Bio-yield ({BIO_YIELD/1e3:.0f} kPa)")
ax_pressure.set_xlabel("Radial Position r (mm)", fontsize=11)
ax_pressure.set_ylabel("Contact Pressure (kPa)", fontsize=11)
ax_pressure.set_title(f"Pressure Distribution (F = {F_ref:.0f} N)", fontsize=12)
ax_pressure.legend(fontsize=9)
ax_pressure.grid(True, alpha=0.3)

# 텍스트 정보 박스
info_text = ax_pressure.text(0.98, 0.95, "", transform=ax_pressure.transAxes,
                              fontsize=10, verticalalignment="top", horizontalalignment="right",
                              bbox=dict(boxstyle="round,pad=0.5", facecolor="lightyellow", alpha=0.8))

def update_info(a_val, p0_val, sigma_max, safety):
    sf_mark = "O" if safety >= 1.5 else ("!" if safety >= 1.0 else "X")
    info_text.set_text(
        f"a = {a_val*1e3:.3f} mm\n"
        f"p_0 = {p0_val/1e3:.1f} kPa\n"
        f"σ_max = {sigma_max/1e3:.1f} kPa\n"
        f"Safety: {sf_mark} {safety:.2f}"
    )

update_info(a_ref, p0_ref, p0_ref, BIO_YIELD / p0_ref)

# ============================================================
# 4. 슬라이더 위젯
# ============================================================
ax_R = fig.add_axes([0.08, 0.22, 0.55, 0.03])
ax_E = fig.add_axes([0.08, 0.15, 0.55, 0.03])
ax_nu = fig.add_axes([0.08, 0.08, 0.55, 0.03])

slider_R = Slider(ax_R, "Radius R (mm)", 20, 80, valinit=R_init, valstep=1)
slider_E = Slider(ax_E, "E_fruit (MPa)", 0.5, 20.0, valinit=E_init, valstep=0.5)
slider_nu = Slider(ax_nu, "ν (Poisson)", 0.20, 0.49, valinit=nu_init, valstep=0.01)

# ============================================================
# 5. 라디오 버튼 (접촉면 재질 선택)
# ============================================================
ax_radio = fig.add_axes([0.72, 0.35, 0.25, 0.25])
radio = RadioButtons(ax_radio, list(surface_db.keys()), active=0)
ax_radio.set_title("Contact Surface", fontsize=10, fontweight="bold")

# ============================================================
# 6. 업데이트 콜백
# ============================================================
def update(val=None):
    global current_surface
    
    R_m = slider_R.val * 1e-3
    E_fruit_Pa = slider_E.val * 1e6
    nu_val = slider_nu.val
    surf = surface_db[current_surface]
    
    E_star = calc_E_star(E_fruit_Pa, nu_val, surf["E"], surf["nu"])
    R_star = R_m
    
    # F-δ 곡선 업데이트
    delta_new, sigma_new, a_new = hertz_Fd(F_arr, R_star, E_star)
    line_fd.set_xdata(delta_new * 1e3)
    ax_fd.set_xlim(0, max(delta_new * 1e3) * 1.1)
    
    # 압력 분포 업데이트 (F = 5 N 기준)
    a_ref = (3 * F_ref * R_star / (4 * E_star)) ** (1/3)
    p0_ref = 3 * F_ref / (2 * np.pi * a_ref**2)
    r_new = np.linspace(-a_ref * 1.5, a_ref * 1.5, 500)
    p_new = np.where(np.abs(r_new) <= a_ref,
                      p0_ref * np.sqrt(1 - (r_new / a_ref)**2), 0)
    
    line_p.set_xdata(r_new * 1e3)
    line_p.set_ydata(p_new / 1e3)
    ax_pressure.set_xlim(min(r_new * 1e3) * 1.1, max(r_new * 1e3) * 1.1)
    ax_pressure.set_ylim(0, max(p0_ref / 1e3 * 1.3, BIO_YIELD / 1e3 * 1.1))
    
    safety = BIO_YIELD / p0_ref
    update_info(a_ref, p0_ref, p0_ref, safety)
    
    fig.canvas.draw_idle()

def on_radio(label):
    global current_surface
    current_surface = label
    update()

slider_R.on_changed(update)
slider_E.on_changed(update)
slider_nu.on_changed(update)
radio.on_clicked(on_radio)

print("=" * 55)
print("  인터랙티브 접촉 응력 시뮬레이터 구동 중...")
print("  → 슬라이더로 R, E, ν 조절")
print("  → 라디오 버튼으로 접촉면 재질 전환")
print("  → Bio-yield 대비 안전율 실시간 확인")
print("=" * 55)

plt.show()
