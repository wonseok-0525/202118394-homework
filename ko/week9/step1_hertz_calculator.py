"""
[Step 1] 헤르츠 접촉 응력 계산기 (Hertz Contact Stress Calculator)
- 9주차 실습: 기계적 특성 I — 접촉 응력과 헤르츠 이론
- 구형 과일-평판/구형 과일 간 접촉 시 접촉 반경, 침투 깊이, 최대 응력 자동 산출
- 접촉면 재질(스테인리스/고무/실리콘) 별 비교 분석 포함
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# ============================================================
# 1. 헤르츠 접촉 핵심 함수
# ============================================================
def hertz_contact(F, R_star, E_star):
    """
    헤르츠 접촉 해석
    Parameters:
        F       : 접촉 하중 (N)
        R_star  : 등가 곡률 반경 (m)
        E_star  : 복합 탄성 계수 (Pa)
    Returns:
        a       : 접촉 반경 (m)
        delta   : 침투 깊이 (m)
        sigma_max: 최대 접촉 응력 (Pa)
    """
    a = (3 * F * R_star / (4 * E_star)) ** (1/3)
    delta = a**2 / R_star
    sigma_max = 3 * F / (2 * np.pi * a**2)
    return a, delta, sigma_max


def combined_elastic_modulus(E1, nu1, E2, nu2):
    """복합 탄성 계수 E* 산출"""
    return 1.0 / ((1 - nu1**2) / E1 + (1 - nu2**2) / E2)


# ============================================================
# 2. 과일 물성 데이터 (사과 Fuji 기준)
# ============================================================
R_fruit = 0.040       # 과일 반경 40 mm → m
E_fruit = 5.0e6       # 영률 5 MPa
nu_fruit = 0.33       # 포아송 비

print("=" * 65)
print("  🔬 헤르츠 접촉 응력 계산기 — 9주차 실습 Step 1")
print("=" * 65)
print(f"\n  📌 과일 물성 (사과 Fuji)")
print(f"     반경 R = {R_fruit*1e3:.0f} mm")
print(f"     영률 E = {E_fruit/1e6:.1f} MPa")
print(f"     포아송 비 ν = {nu_fruit}")

# ============================================================
# 3. 접촉면 재질 비교 분석
# ============================================================
surfaces = {
    "스테인리스 강":   {"E": 200e9,   "nu": 0.30, "color": "#e74c3c"},
    "경질 고무":       {"E": 30e6,    "nu": 0.45, "color": "#e67e22"},
    "연질 실리콘":     {"E": 2e6,     "nu": 0.48, "color": "#2ecc71"},
    "에어 쿠션":       {"E": 0.05e6,  "nu": 0.49, "color": "#3498db"},
}

# 구-평면 접촉: R* = R_fruit (평판의 R = ∞)
R_star = R_fruit
F_load = 3.0  # 접촉 하중 3 N (약 300g 자중)

print(f"\n  📌 접촉 조건: 구-평면 접촉 (하중 F = {F_load:.1f} N)")
print("-" * 65)
print(f"  {'접촉면 재질':<14} {'E*':>10} {'접촉반경 a':>12} {'침투깊이 δ':>12} {'σ_max':>12} {'안전율':>8}")
print(f"  {'':14} {'(MPa)':>10} {'(mm)':>12} {'(mm)':>12} {'(kPa)':>12} {'':>8}")
print("-" * 65)

bio_yield = 300e3  # Bio-yield Stress: 300 kPa

results = {}
for name, props in surfaces.items():
    E_star = combined_elastic_modulus(E_fruit, nu_fruit, props["E"], props["nu"])
    a, delta, sigma_max = hertz_contact(F_load, R_star, E_star)
    safety_factor = bio_yield / sigma_max
    results[name] = {"a": a, "delta": delta, "sigma_max": sigma_max, 
                     "E_star": E_star, "safety": safety_factor, "color": props["color"]}
    
    sf_mark = "O" if safety_factor >= 1.5 else ("!" if safety_factor >= 1.0 else "X")
    print(f"  {name:<14} {E_star/1e6:>10.2f} {a*1e3:>12.3f} {delta*1e3:>12.4f} {sigma_max/1e3:>12.1f} {sf_mark}{safety_factor:>6.2f}")

print("-" * 65)
print(f"  ※ Bio-yield Stress (사과 Fuji) = {bio_yield/1e3:.0f} kPa")
print(f"  ※ 안전율 ≥ 1.5: O 안전 / 1.0~1.5: ! 주의 / < 1.0: X 위험")

# ============================================================
# 4. 하중 변화에 따른 접촉 반경 및 최대 응력 트렌드 그래프
# ============================================================
F_range = np.linspace(0.1, 20.0, 200)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
fig.suptitle("Hertz Contact Analysis — Surface Material Comparison", 
             fontsize=14, fontweight="bold")

for name, res in results.items():
    E_star = res["E_star"]
    a_arr = (3 * F_range * R_star / (4 * E_star)) ** (1/3)
    sigma_arr = 3 * F_range / (2 * np.pi * a_arr**2)
    
    ax1.plot(F_range, a_arr * 1e3, label=name, color=res["color"], linewidth=2)
    ax2.plot(F_range, sigma_arr / 1e3, label=name, color=res["color"], linewidth=2)

# Bio-yield 기준선
ax2.axhline(y=bio_yield/1e3, color="gray", linestyle="--", linewidth=1.5, label=f"Bio-yield ({bio_yield/1e3:.0f} kPa)")

ax1.set_xlabel("Contact Force F (N)", fontsize=12)
ax1.set_ylabel("Contact Radius a (mm)", fontsize=12)
ax1.set_title("Contact Radius vs Load", fontsize=12)
ax1.legend(fontsize=9)
ax1.grid(True, alpha=0.3)

ax2.set_xlabel("Contact Force F (N)", fontsize=12)
ax2.set_ylabel("Maximum Stress σ_max (kPa)", fontsize=12)
ax2.set_title("Maximum Contact Stress vs Load", fontsize=12)
ax2.legend(fontsize=9)
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("step1_result.png", dpi=150, bbox_inches="tight")
plt.show()

print("\n  📊 그래프가 step1_result.png 으로 저장됨")
print("=" * 65)
