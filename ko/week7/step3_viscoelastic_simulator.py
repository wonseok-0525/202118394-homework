"""
[Step 3] 인터랙티브 점탄성 시뮬레이터 (Interactive Viscoelastic Simulator)
- 7주차 실습: 점탄성 특성 — 크리프와 응력 이완
- 모델 전환 라디오 버튼: Maxwell / Kelvin-Voigt / Burgers
- 파라미터 슬라이더: E₁, E₂, η₁, η₂ 실시간 조절
- 듀얼 플로팅: 좌측(크리프 곡선) + 우측(응력 이완 곡선)
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False
from matplotlib.widgets import Slider, RadioButtons

# ============================================================
# 1. 점탄성 모델 수식
# ============================================================
SIGMA_0 = 10.0   # 일정 응력 (kPa) — 크리프용
EPS_0 = 0.05     # 일정 변형률 5% — 응력 이완용

def maxwell_creep(t, E1, eta1):
    return SIGMA_0 / E1 + (SIGMA_0 / eta1) * t

def maxwell_relaxation(t, E1, eta1):
    sigma_init = E1 * EPS_0
    tau_r = eta1 / E1
    return sigma_init * np.exp(-t / tau_r)

def kv_creep(t, E2, eta2):
    tau_c = eta2 / E2
    return (SIGMA_0 / E2) * (1 - np.exp(-t / tau_c))

def kv_relaxation(t, E2, eta2):
    # KV 모델은 응력 이완을 제대로 묘사 못함 — 즉시 완전 이완 근사
    return np.full_like(t, E2 * EPS_0)

def burgers_creep(t, E1, E2, eta1, eta2):
    instant = SIGMA_0 / E1
    delayed = (SIGMA_0 / E2) * (1 - np.exp(-t * E2 / eta2))
    viscous = (SIGMA_0 / eta1) * t
    return instant + delayed + viscous

def burgers_relaxation(t, E1, E2, eta1, eta2):
    # Burgers 응력 이완 — 근사: 2-term 지수 감쇠
    sigma_init = E1 * EPS_0
    tau1 = eta1 / E1
    tau2 = eta2 / E2
    return sigma_init * (0.6 * np.exp(-t / tau1) + 0.4 * np.exp(-t / tau2))

# ============================================================
# 2. 초기 파라미터
# ============================================================
E1_init = 200.0   # kPa
E2_init = 100.0   # kPa
eta1_init = 3000.0  # kPa·s
eta2_init = 500.0   # kPa·s
current_model = "Burgers"

t = np.linspace(0.01, 120, 500)

# ============================================================
# 3. 그래프 초기 설정
# ============================================================
fig, (ax_creep, ax_relax) = plt.subplots(1, 2, figsize=(15, 6))
fig.subplots_adjust(left=0.08, right=0.68, bottom=0.35, top=0.88)
fig.suptitle("Interactive Viscoelastic Simulator", fontsize=14, fontweight="bold")

# 초기 곡선 계산
creep_data = burgers_creep(t, E1_init, E2_init, eta1_init, eta2_init)
relax_data = burgers_relaxation(t, E1_init, E2_init, eta1_init, eta2_init)

line_creep, = ax_creep.plot(t, creep_data, "b-", linewidth=2)
ax_creep.set_xlabel("Time (s)", fontsize=11)
ax_creep.set_ylabel("Strain $\epsilon$ (%)", fontsize=11)
ax_creep.set_title("Creep Curve ($\sigma_0$ = 10 kPa)", fontsize=12)
ax_creep.grid(True, alpha=0.3)

line_relax, = ax_relax.plot(t, relax_data, "r-", linewidth=2)
ax_relax.set_xlabel("Time (s)", fontsize=11)
ax_relax.set_ylabel("Stress $\sigma(t)$ (kPa)", fontsize=11)
ax_relax.set_title("Stress Relaxation ($\epsilon_0$ = 5%)", fontsize=12)
ax_relax.grid(True, alpha=0.3)

# 정보 박스
info_text = fig.text(0.70, 0.75, "", fontsize=10,
                     bbox=dict(boxstyle="round,pad=0.5", facecolor="lightyellow", alpha=0.9))

def update_info(model, E1, E2, eta1, eta2):
    tau1 = eta1 / E1
    tau2 = eta2 / E2 if E2 > 0 else 0
    info_text.set_text(
        f"모델: {model}\n"
        f"$\\tau_1$(Maxwell) = {tau1:.1f} s\n"
        f"$\\tau_2$(KV) = {tau2:.1f} s\n"
        f"즉시탄성 = {SIGMA_0/E1:.3f} %\n"
        f"점성기울기 = {SIGMA_0/eta1:.5f} %/s"
    )

update_info(current_model, E1_init, E2_init, eta1_init, eta2_init)

# ============================================================
# 4. 슬라이더 위젯
# ============================================================
ax_E1 = fig.add_axes([0.08, 0.22, 0.55, 0.03])
ax_E2 = fig.add_axes([0.08, 0.16, 0.55, 0.03])
ax_eta1 = fig.add_axes([0.08, 0.10, 0.55, 0.03])
ax_eta2 = fig.add_axes([0.08, 0.04, 0.55, 0.03])

slider_E1 = Slider(ax_E1, "$E_1$ (kPa)", 50, 500, valinit=E1_init, valstep=10)
slider_E2 = Slider(ax_E2, "$E_2$ (kPa)", 30, 300, valinit=E2_init, valstep=10)
slider_eta1 = Slider(ax_eta1, "$\eta_1$ (kPa·s)", 500, 10000, valinit=eta1_init, valstep=100)
slider_eta2 = Slider(ax_eta2, "$\eta_2$ (kPa·s)", 100, 2000, valinit=eta2_init, valstep=50)

# ============================================================
# 5. 라디오 버튼 (모델 선택)
# ============================================================
ax_radio = fig.add_axes([0.70, 0.35, 0.25, 0.20])
radio = RadioButtons(ax_radio, ["Maxwell", "Kelvin-Voigt", "Burgers"], active=2)
ax_radio.set_title("Model Selection", fontsize=10, fontweight="bold")

# ============================================================
# 6. 업데이트 콜백
# ============================================================
def update(val=None):
    global current_model
    E1 = slider_E1.val
    E2 = slider_E2.val
    eta1 = slider_eta1.val
    eta2 = slider_eta2.val
    
    if current_model == "Maxwell":
        creep = maxwell_creep(t, E1, eta1)
        relax = maxwell_relaxation(t, E1, eta1)
    elif current_model == "Kelvin-Voigt":
        creep = kv_creep(t, E2, eta2)
        relax = kv_relaxation(t, E2, eta2)
    else:  # Burgers
        creep = burgers_creep(t, E1, E2, eta1, eta2)
        relax = burgers_relaxation(t, E1, E2, eta1, eta2)
    
    line_creep.set_ydata(creep)
    line_relax.set_ydata(relax)
    
    ax_creep.set_ylim(0, max(creep) * 1.15)
    ax_relax.set_ylim(0, max(relax) * 1.15)
    
    update_info(current_model, E1, E2, eta1, eta2)
    fig.canvas.draw_idle()

def on_radio(label):
    global current_model
    current_model = label
    update()

slider_E1.on_changed(update)
slider_E2.on_changed(update)
slider_eta1.on_changed(update)
slider_eta2.on_changed(update)
radio.on_clicked(on_radio)

print("=" * 55)
print("  🎛️ 인터랙티브 점탄성 시뮬레이터 구동 중...")
print("  → 슬라이더: E₁, E₂, η₁, η₂ 실시간 조절")
print("  → 라디오 버튼: Maxwell / KV / Burgers 전환")
print("  → 듀얼 플롯: 크리프(좌) + 응력 이완(우)")
print("=" * 55)

plt.show()
