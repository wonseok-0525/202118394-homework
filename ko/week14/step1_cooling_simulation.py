import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from matplotlib.widgets import Slider, RadioButtons, CheckButtons
from scipy.integrate import solve_ivp
import os

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 9

# ============================================================
# 14주차 심화 실습: 열적 특성 — 호흡열을 고려한 1D 구형 냉각 시뮬레이션
# ============================================================

# 품목별 열물성 프리셋 및 에셋 경로 (실제 파일 포맷인 jpg로 수정)
PRODUCT_DATA = {
    '사과 (Apple)': {'k': 0.42, 'rho': 840, 'cp': 3800, 'q_a': 0.005, 'q_b': 0.10, 'img': 'apple.jpg'},
    '감자 (Potato)': {'k': 0.55, 'rho': 1050, 'cp': 3500, 'q_a': 0.008, 'q_b': 0.08, 'img': 'potato.jpg'},
    '포도 (Grape)': {'k': 0.52, 'rho': 1080, 'cp': 3700, 'q_a': 0.004, 'q_b': 0.12, 'img': 'grape.jpg'},
    '토마토 (Tomato)': {'k': 0.60, 'rho': 950, 'cp': 4000, 'q_a': 0.007, 'q_b': 0.11, 'img': 'tomato.jpg'},
}

DEFAULT_PARAMS = {
    'product': '사과 (Apple)',
    'R': 0.04,
    'h': 25.0,
    'T_init': 25.0,
    'T_inf': 2.0,
    'use_resp': True,
    'N': 40,
    't_end': 10800,
}

def build_ode_system(params):
    p = PRODUCT_DATA[params['product']]
    k, rho, cp = p['k'], p['rho'], p['cp']
    q_a, q_b = p['q_a'], p['q_b']
    R, h, T_inf, N = params['R'], params['h'], params['T_inf'], params['N']
    use_resp = params['use_resp']
    alpha = k / (rho * cp)
    dr = R / N
    r = np.linspace(0, R, N + 1)

    def dTdt(t, T):
        dT = np.zeros_like(T)
        resp_term = (q_a * np.exp(q_b * T)) / cp if use_resp else 0.0
        for i in range(1, N):
            d2T_dr2 = (T[i + 1] - 2 * T[i] + T[i - 1]) / dr**2
            dT_dr = (T[i + 1] - T[i - 1]) / (2 * dr)
            dT[i] = alpha * (d2T_dr2 + (2 / r[i]) * dT_dr) + resp_term[i]
        d2T_center = (T[1] - T[0]) / dr**2
        dT[0] = alpha * 3 * d2T_center + resp_term[0]
        T_surf = (k * T[N - 1] + h * dr * T_inf) / (k + h * dr)
        T[N] = T_surf
        dT[N] = (alpha * (T[N-1] - 2*T[N] + T[N])/dr**2) + resp_term[N]
        return dT
    return r, dTdt

def run_sim(params):
    T_init, t_end = params['T_init'], params['t_end']
    r, dTdt = build_ode_system(params)
    T0 = np.full(len(r), T_init)
    t_eval = np.linspace(0, t_end, 300)
    sol = solve_ivp(dTdt, [0, t_end], T0, t_eval=t_eval, method='RK45')
    T_center = sol.y[0, :] + 0.15 * np.random.randn(len(t_eval))
    T_surface = sol.y[-1, :] + 0.10 * np.random.randn(len(t_eval))
    return t_eval, T_center, T_surface, sol.y, r

def main():
    params = DEFAULT_PARAMS.copy()
    base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets')
    
    t_eval, T_c, T_s, T_all, r_grid = run_sim(params)
    fig = plt.figure(figsize=(16, 9))
    plt.subplots_adjust(left=0.07, right=0.85, bottom=0.25, top=0.92, wspace=0.25, hspace=0.35)

    # 1. 온도 시계열
    ax1 = fig.add_subplot(2, 3, 1)
    line_c, = ax1.plot(t_eval/60, T_c, 'b-', alpha=0.7, label='중심')
    line_s, = ax1.plot(t_eval/60, T_s, 'r--', alpha=0.7, label='표면')
    ax1.axhline(params['T_inf'], color='k', ls=':', label='냉매')
    ax1.set_title('시간별 온도 변화')
    ax1.set_xlabel('시간 (min)')
    ax1.set_ylabel('온도 (°C)')
    ax1.legend(loc='upper right', fontsize=8)

    # 2. 무차원 온도
    ax2 = fig.add_subplot(2, 3, 2)
    theta = (T_c - params['T_inf']) / (params['T_init'] - params['T_inf'])
    line_theta, = ax2.plot(t_eval/60, theta, 'g-', lw=2)
    ax2.set_title('무차원 온도 지수 (θ)')
    ax2.set_ylim(-0.05, 1.05)

    # 3. 이미지 표시 영역 (PIL 사용)
    ax_img = fig.add_subplot(2, 3, 3)
    ax_img.axis('off')
    img_disp = None
    
    def load_product_img(product_name):
        img_name = PRODUCT_DATA[product_name]['img']
        path = os.path.join(base_path, img_name)
        if os.path.exists(path):
            try:
                return Image.open(path)
            except:
                return None
        return None

    img_data = load_product_img(params['product'])
    if img_data is not None:
        img_disp = ax_img.imshow(img_data)
    else:
        ax_img.text(0.5, 0.5, 'Image not found', ha='center')
    ax_img.set_title('실습 대상 품목')

    # 4. 공간적 분포
    ax3 = fig.add_subplot(2, 3, 4)
    times_to_plot = [0, 10, 30, 60, 120]
    profile_lines = []
    for tm in times_to_plot:
        idx = np.argmin(np.abs(t_eval - tm*60))
        ln, = ax3.plot(r_grid*100, T_all[:, idx], label=f'{tm} min')
        profile_lines.append(ln)
    ax3.set_title('반경 방향 온도 분포')
    ax3.set_xlabel('반경 (cm)')
    ax3.set_ylabel('온도 (°C)')
    ax3.legend(loc='lower left', fontsize=8)

    # 5. 분석 결과
    ax4 = fig.add_subplot(2, 3, 5)
    ax4.axis('off')
    res_text = ax4.text(0.1, 0.5, '', fontsize=10, transform=ax4.transAxes, 
                        bbox=dict(facecolor='white', alpha=0.8))

    def update_text(p, tc_data):
        bi = p['h'] * p['R'] / PRODUCT_DATA[p['product']]['k']
        hct_idx = np.where((tc_data - p['T_inf']) / (p['T_init'] - p['T_inf']) <= 0.5)[0]
        hct = t_eval[hct_idx[0]]/60 if len(hct_idx) > 0 else 999
        txt = (f"[분석 리포트]\n- 품목: {p['product']}\n- Bi: {bi:.3f}\n- HCT: {hct:.1f} min\n"
               f"- 호흡열: {'ON' if p['use_resp'] else 'OFF'}\n- 최종온도: {tc_data[-1]:.2f} °C")
        res_text.set_text(txt)

    update_text(params, T_c)

    # 컨트롤 위젯
    ax_h = plt.axes([0.1, 0.12, 0.3, 0.02])
    ax_r = plt.axes([0.1, 0.08, 0.3, 0.02])
    ax_ti = plt.axes([0.1, 0.04, 0.3, 0.02])
    s_h = Slider(ax_h, '대류계수', 5, 100, valinit=params['h'])
    s_r = Slider(ax_r, '반경(cm)', 2, 10, valinit=params['R']*100)
    s_ti = Slider(ax_ti, '초기온도', 10, 40, valinit=params['T_init'])

    ax_radio = plt.axes([0.45, 0.02, 0.12, 0.15], facecolor='#f9f9f9')
    radio = RadioButtons(ax_radio, list(PRODUCT_DATA.keys()))

    ax_check = plt.axes([0.6, 0.05, 0.1, 0.08], facecolor='#f9f9f9')
    check = CheckButtons(ax_check, ['호흡열'], [True])

    def update(val):
        params['h'] = s_h.val
        params['R'] = s_r.val / 100.0
        params['T_init'] = s_ti.val
        params['product'] = radio.value_selected
        params['use_resp'] = check.get_status()[0]

        te, tc, ts, tall, rg = run_sim(params)
        line_c.set_data(te/60, tc)
        line_s.set_data(te/60, ts)
        ax1.set_ylim(0, params['T_init'] + 3)
        line_theta.set_data(te/60, (tc - params['T_inf']) / (params['T_init'] - params['T_inf']))
        
        for i, tm in enumerate(times_to_plot):
            idx = np.argmin(np.abs(te - tm*60))
            profile_lines[i].set_data(rg*100, tall[:, idx])
        ax3.set_ylim(params['T_inf']-1, params['T_init']+1)
        
        # 이미지 업데이트
        new_img = load_product_img(params['product'])
        if new_img is not None:
            img_disp.set_data(new_img)
        
        update_text(params, tc)
        fig.canvas.draw_idle()

    s_h.on_changed(update)
    s_r.on_changed(update)
    s_ti.on_changed(update)
    radio.on_clicked(update)
    check.on_clicked(update)

    plt.suptitle('14주차 실습: 생물자원 냉각 디지털 트윈 시뮬레이터', fontsize=14)
    plt.show()

if __name__ == '__main__':
    main()
