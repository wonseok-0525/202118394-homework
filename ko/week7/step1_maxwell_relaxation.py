"""
[Step 1] Maxwell 응력 이완 시뮬레이션 (Maxwell Stress Relaxation Simulation)
- 7주차 실습: 점탄성 특성 — 크리프와 응력 이완
- 단일 지수 감쇠 곡선 σ(t) = σ₀·exp(-t/τᵣ) 생성
- 3가지 η 값에 대한 이완 곡선 비교 및 τᵣ 감도 분석
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# ============================================================
# 1. Maxwell 응력 이완 함수
# ============================================================
def maxwell_relaxation(t, sigma_0, E, eta):
    """
    Maxwell 모델 응력 이완
    Parameters:
        t       : 시간 배열 (s)
        sigma_0 : 초기 응력 (kPa)
        E       : 영률 (kPa)
        eta     : 점성 계수 (kPa·s)
    Returns:
        sigma_t : 시간에 따른 응력 (kPa)
    """
    tau_r = eta / E  # 이완 시간
    sigma_t = sigma_0 * np.exp(-t / tau_r)
    return sigma_t, tau_r


# ============================================================
# 2. 파라미터 설정 — 사과(Fuji) 기반 가상 데이터
# ============================================================
sigma_0 = 50.0   # 초기 응력 (kPa)
E = 300.0        # 영률 (kPa)
t = np.linspace(0, 60, 500)  # 0~60초

# 3가지 점성 계수 비교
eta_values = [600, 1200, 3000]  # kPa·s
colors = ["#e74c3c", "#2980b9", "#27ae60"]
labels_kr = ["낮은 점성 (η=600)", "중간 점성 (η=1200)", "높은 점성 (η=3000)"]

print("=" * 60)
print("  🔩 Maxwell 응력 이완 시뮬레이션 — 7주차 실습 Step 1")
print("=" * 60)
print(f"\n  📌 공통 파라미터")
print(f"     초기 응력 σ₀ = {sigma_0:.1f} kPa")
print(f"     영률 E = {E:.0f} kPa")
print(f"\n  {'점성 계수 η':>15} {'이완 시간 τᵣ':>15} {'σ(30s)':>12} {'σ(60s)':>12}")
print(f"  {'(kPa·s)':>15} {'(s)':>15} {'(kPa)':>12} {'(kPa)':>12}")
print("-" * 60)

# ============================================================
# 3. 시뮬레이션 및 플로팅
# ============================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
fig.suptitle("Maxwell Stress Relaxation — $\eta$ Sensitivity Analysis",
             fontsize=14, fontweight="bold")

for eta, color, label in zip(eta_values, colors, labels_kr):
    sigma_t, tau_r = maxwell_relaxation(t, sigma_0, E, eta)
    
    # 콘솔 출력
    sigma_30 = sigma_0 * np.exp(-30 / tau_r)
    sigma_60 = sigma_0 * np.exp(-60 / tau_r)
    print(f"  {eta:>15.0f} {tau_r:>15.1f} {sigma_30:>12.2f} {sigma_60:>12.2f}")
    
    # 좌측: 응력 이완 곡선
    ax1.plot(t, sigma_t, color=color, linewidth=2, label=f"{label}\n$\\tau_r$ = {tau_r:.1f} s")
    
    # τᵣ 지점 마커 표시
    sigma_at_tau = sigma_0 * np.exp(-1)  # σ₀/e
    ax1.plot(tau_r, sigma_at_tau, "o", color=color, markersize=8)

# $\sigma_0$/e 수평선
ax1.axhline(y=sigma_0 / np.e, color="gray", linestyle="--", linewidth=1,
            label=f"$\sigma_0$/e = {sigma_0/np.e:.1f} kPa")

ax1.set_xlabel("Time (s)", fontsize=12)
ax1.set_ylabel("Stress σ(t) (kPa)", fontsize=12)
ax1.set_title("Stress Relaxation Curves", fontsize=12)
ax1.legend(fontsize=9, loc="upper right")
ax1.grid(True, alpha=0.3)
ax1.set_xlim(0, 60)
ax1.set_ylim(0, sigma_0 * 1.05)

# 우측: 이완 탄성률 E(t)
epsilon_0 = sigma_0 / E  # 초기 변형률
for eta, color, label in zip(eta_values, colors, labels_kr):
    tau_r = eta / E
    E_t = E * np.exp(-t / tau_r)
    ax2.plot(t, E_t, color=color, linewidth=2, label=label)

ax2.set_xlabel("Time (s)", fontsize=12)
ax2.set_ylabel("Relaxation Modulus E(t) (kPa)", fontsize=12)
ax2.set_title("Relaxation Modulus E(t) = E $\cdot$ exp(-t/$\\tau_r$)", fontsize=12)
ax2.legend(fontsize=9)
ax2.grid(True, alpha=0.3)
ax2.set_xlim(0, 60)

print("-" * 60)
print(f"\n  ※ σ₀/e 기준점 = {sigma_0/np.e:.2f} kPa")
print(f"  ※ 이완 시간(τᵣ) 지점에서 응력이 초기값의 ~36.8%로 감소")

plt.tight_layout()
plt.savefig("step1_result.png", dpi=150, bbox_inches="tight")
plt.show()

print(f"\n  📊 그래프가 step1_result.png 으로 저장됨")
print("=" * 60)
