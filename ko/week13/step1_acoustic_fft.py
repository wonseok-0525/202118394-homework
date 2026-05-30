import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from scipy.signal import find_peaks
import pandas as pd
import os

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 10

# ============================================================
# 13주차 실습: 음향 특성 — FFT 기반 경도 분석
# ============================================================


def generate_impact_signal(f_resonance, damping, mass, sr=44100, duration=0.3):
    """가상 타격 응답 신호 생성"""
    t = np.linspace(0, duration, int(sr * duration), endpoint=False)
    envelope = np.exp(-damping * t)
    main_tone = envelope * np.sin(2 * np.pi * f_resonance * t)
    harmonic = 0.15 * envelope * np.sin(2 * np.pi * f_resonance * 2.1 * t)
    noise = 0.02 * np.random.randn(len(t))
    signal = main_tone + harmonic + noise
    return t, signal


def compute_fft(signal, sr):
    """FFT 변환 → 양(Positive) 주파수 영역 추출"""
    N = len(signal)
    fft_vals = np.fft.rfft(signal)
    magnitude = np.abs(fft_vals) * 2.0 / N
    freqs = np.fft.rfftfreq(N, d=1.0 / sr)
    return freqs, magnitude


def detect_peak(freqs, magnitude, min_freq=50, max_freq=5000, height_ratio=0.3):
    """공명 피크 자동 검출 — scipy.signal.find_peaks 활용"""
    mask = (freqs >= min_freq) & (freqs <= max_freq)
    freqs_crop = freqs[mask]
    mag_crop = magnitude[mask]
    threshold = height_ratio * np.max(mag_crop)
    peaks, _ = find_peaks(mag_crop, height=threshold, distance=20)
    if len(peaks) == 0:
        idx = np.argmax(mag_crop)
        return freqs_crop[idx], mag_crop[idx]
    dominant = peaks[np.argmax(mag_crop[peaks])]
    return freqs_crop[dominant], mag_crop[dominant]


def calc_stiffness(f_hz, mass_g):
    """경도 지수 S = f² × m^(2/3), 질량 kg 변환"""
    mass_kg = mass_g / 1000.0
    return (f_hz ** 2) * (mass_kg ** (2 / 3))


def classify_firmness(S):
    """등급 분류"""
    if S > 2e5:
        return '단단함 (Firm)'
    elif S > 8e4:
        return '보통 (Medium)'
    else:
        return '물러짐 (Soft)'


def main():
    np.random.seed(42)
    sr = 44100
    num_samples = 30

    # 성숙도별 공명 주파수 분포
    f_resonances = np.concatenate([
        np.random.uniform(600, 900, 10),   # 단단함
        np.random.uniform(400, 600, 10),   # 보통
        np.random.uniform(200, 400, 10),   # 물러짐
    ])
    dampings = np.random.uniform(15, 40, num_samples)
    masses = np.random.uniform(150, 350, num_samples)

    # 전체 샘플 FFT 분석
    results = []
    for i in range(num_samples):
        t, sig = generate_impact_signal(f_resonances[i], dampings[i], masses[i], sr=sr)
        freqs, mag = compute_fft(sig, sr)
        peak_f, peak_m = detect_peak(freqs, mag)
        S = calc_stiffness(peak_f, masses[i])
        grade = classify_firmness(S)
        results.append({
            'Sample': i + 1, 'Mass_g': round(masses[i], 1),
            'True_f_Hz': round(f_resonances[i], 1),
            'Detected_f_Hz': round(peak_f, 1),
            'Stiffness': round(S, 0), 'Grade': grade
        })

    df = pd.DataFrame(results)
    print("=" * 70)
    print("  13주차 실습: 음향 FFT 기반 경도 지수 분석 결과")
    print("=" * 70)
    print(df.to_string(index=False))
    print(f"\n총 {num_samples}개 샘플 분석 완료\n")

    # CSV 저장
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, 'data')
    os.makedirs(data_dir, exist_ok=True)
    csv_path = os.path.join(data_dir, 'acoustic_results.csv')
    df.to_csv(csv_path, index=False, encoding='utf-8-sig')
    print(f"결과 저장 완료: {csv_path}\n")

    # 시각화: 4패널 — 범례 클릭 시 해당 등급 강조(진하게) 표시
    sample_indices = [0, 10, 20]
    sample_labels = ['단단함 (Firm)', '보통 (Medium)', '물러짐 (Soft)']
    sample_colors = ['#2196F3', '#FF9800', '#F44336']

    fig, axes = plt.subplots(2, 2, figsize=(16, 10))
    plt.subplots_adjust(bottom=0.18, hspace=0.35, wspace=0.3)

    # 모든 패널의 아티스트를 등급별로 관리 (범례 클릭 강조용)
    # key: grade label → value: list of artists
    grade_artists = {label: [] for label in sample_labels}

    # 기본/강조/페이드 스타일 상수
    ALPHA_DEFAULT = 0.8
    ALPHA_HIGHLIGHT = 1.0
    ALPHA_FADE = 0.12
    LW_DEFAULT_LINE = 0.8
    LW_HIGHLIGHT_LINE = 2.5
    LW_DEFAULT_FFT = 1.0
    LW_HIGHLIGHT_FFT = 2.8
    SIZE_DEFAULT = 60
    SIZE_HIGHLIGHT = 120

    # (0,0) 시간 도메인 파형
    ax_wave = axes[0, 0]
    for idx, label, color in zip(sample_indices, sample_labels, sample_colors):
        t, sig = generate_impact_signal(f_resonances[idx], dampings[idx], masses[idx], sr=sr)
        line, = ax_wave.plot(t * 1000, sig, alpha=ALPHA_DEFAULT, label=label,
                             color=color, linewidth=LW_DEFAULT_LINE)
        grade_artists[label].append(('line', line, LW_DEFAULT_LINE))
    ax_wave.set_title('Time Domain — Impact Response Waveform')
    ax_wave.set_xlabel('Time (ms)')
    ax_wave.set_ylabel('Amplitude')
    leg_wave = ax_wave.legend(loc='upper right', fontsize=9)
    ax_wave.grid(True, linestyle=':', alpha=0.5)

    # (0,1) FFT 스펙트럼
    ax_fft = axes[0, 1]
    fft_annotations = {label: [] for label in sample_labels}
    for idx, label, color in zip(sample_indices, sample_labels, sample_colors):
        t, sig = generate_impact_signal(f_resonances[idx], dampings[idx], masses[idx], sr=sr)
        freqs, mag = compute_fft(sig, sr)
        mask = freqs <= 2000
        line, = ax_fft.plot(freqs[mask], mag[mask], alpha=ALPHA_DEFAULT, label=label,
                            color=color, linewidth=LW_DEFAULT_FFT)
        grade_artists[label].append(('line', line, LW_DEFAULT_FFT))
        pf, pm = detect_peak(freqs, mag)
        ann = ax_fft.annotate(f'{pf:.0f} Hz', xy=(pf, pm), fontsize=8,
                              arrowprops=dict(arrowstyle='->', color=color, lw=1.2),
                              xytext=(pf + 100, pm + 0.01), color=color, fontweight='bold')
        grade_artists[label].append(('annotation', ann, None))
    ax_fft.set_title('Frequency Domain — FFT Power Spectrum')
    ax_fft.set_xlabel('Frequency (Hz)')
    ax_fft.set_ylabel('Magnitude')
    leg_fft = ax_fft.legend(loc='upper right', fontsize=9)
    ax_fft.grid(True, linestyle=':', alpha=0.5)

    # (1,0) 경도 지수 산점도
    ax_scatter = axes[1, 0]
    grade_colors = {'단단함 (Firm)': '#2196F3', '보통 (Medium)': '#FF9800', '물러짐 (Soft)': '#F44336'}
    for grade, color in grade_colors.items():
        subset = df[df['Grade'] == grade]
        sc = ax_scatter.scatter(subset['Detected_f_Hz'], subset['Stiffness'],
                                c=color, label=grade, alpha=ALPHA_DEFAULT,
                                edgecolors='k', linewidth=0.5, s=SIZE_DEFAULT)
        grade_artists[grade].append(('scatter', sc, SIZE_DEFAULT))
    ax_scatter.set_title('Stiffness Coefficient vs Resonance Frequency')
    ax_scatter.set_xlabel('Detected Resonance Frequency (Hz)')
    ax_scatter.set_ylabel('Stiffness Index  S = f² × m^(2/3)')
    leg_scatter = ax_scatter.legend(loc='upper left', fontsize=9)
    ax_scatter.grid(True, linestyle=':', alpha=0.5)
    ax_scatter.axhline(y=2e5, color='#2196F3', linestyle='--', alpha=0.4)
    ax_scatter.axhline(y=8e4, color='#FF9800', linestyle='--', alpha=0.4)

    # (1,1) 질량별 분포
    ax_mass = axes[1, 1]
    for grade, color in grade_colors.items():
        subset = df[df['Grade'] == grade]
        sc = ax_mass.scatter(subset['Mass_g'], subset['Stiffness'],
                             c=color, label=grade, alpha=ALPHA_DEFAULT,
                             edgecolors='k', linewidth=0.5, s=SIZE_DEFAULT)
        grade_artists[grade].append(('scatter', sc, SIZE_DEFAULT))
    ax_mass.set_title('Stiffness Index vs Fruit Mass')
    ax_mass.set_xlabel('Mass (g)')
    ax_mass.set_ylabel('Stiffness Index  S = f² × m^(2/3)')
    leg_mass = ax_mass.legend(loc='upper left', fontsize=9)
    ax_mass.grid(True, linestyle=':', alpha=0.5)

    # ── 범례 클릭 이벤트: 선택 등급 강조, 나머지 페이드 ──
    # 범례 텍스트 → 등급 매핑 구축
    legend_map = {}  # legend text artist → grade label
    all_legends = [leg_wave, leg_fft, leg_scatter, leg_mass]
    for leg in all_legends:
        for leg_text in leg.get_texts():
            leg_text.set_picker(10)
            legend_map[leg_text] = leg_text.get_text()

    active_grade = [None]  # mutable container for closure

    def on_pick(event):
        if event.artist not in legend_map:
            return
        clicked_grade = legend_map[event.artist]

        # 토글: 같은 등급 다시 클릭 → 전체 복원
        if active_grade[0] == clicked_grade:
            active_grade[0] = None
            for grade_label in grade_artists:
                for art_type, art, default_val in grade_artists[grade_label]:
                    if art_type == 'line':
                        art.set_alpha(ALPHA_DEFAULT)
                        art.set_linewidth(default_val)
                    elif art_type == 'scatter':
                        art.set_alpha(ALPHA_DEFAULT)
                        art.set_sizes([default_val])
                    elif art_type == 'annotation':
                        art.set_alpha(ALPHA_DEFAULT)
            # 범례 텍스트 복원
            for leg in all_legends:
                for lt in leg.get_texts():
                    lt.set_alpha(1.0)
                    lt.set_fontweight('normal')
                    lt.set_fontsize(9)
        else:
            active_grade[0] = clicked_grade
            for grade_label in grade_artists:
                is_selected = (grade_label == clicked_grade)
                for art_type, art, default_val in grade_artists[grade_label]:
                    if is_selected:
                        if art_type == 'line':
                            art.set_alpha(ALPHA_HIGHLIGHT)
                            art.set_linewidth(LW_HIGHLIGHT_LINE if default_val == LW_DEFAULT_LINE
                                              else LW_HIGHLIGHT_FFT)
                        elif art_type == 'scatter':
                            art.set_alpha(ALPHA_HIGHLIGHT)
                            art.set_sizes([SIZE_HIGHLIGHT])
                        elif art_type == 'annotation':
                            art.set_alpha(ALPHA_HIGHLIGHT)
                    else:
                        if art_type in ('line', 'scatter'):
                            art.set_alpha(ALPHA_FADE)
                            if art_type == 'line':
                                art.set_linewidth(default_val)
                            elif art_type == 'scatter':
                                art.set_sizes([default_val])
                        elif art_type == 'annotation':
                            art.set_alpha(ALPHA_FADE)
            # 범례 텍스트 강조
            for leg in all_legends:
                for lt in leg.get_texts():
                    if lt.get_text() == clicked_grade:
                        lt.set_alpha(1.0)
                        lt.set_fontweight('bold')
                        lt.set_fontsize(11)
                    else:
                        lt.set_alpha(0.3)
                        lt.set_fontweight('normal')
                        lt.set_fontsize(9)

        fig.canvas.draw_idle()

    fig.canvas.mpl_connect('pick_event', on_pick)

    # 슬라이더: 질량 보정
    ax_slider = plt.axes([0.2, 0.05, 0.6, 0.03], facecolor='lightgoldenrodyellow')
    mass_slider = Slider(ax=ax_slider, label='Mass Override (g)',
                         valmin=100, valmax=500, valinit=250, valstep=10)

    def update(val):
        m_override = mass_slider.val
        detected_fs = df['Detected_f_Hz'].values
        new_s = np.array([calc_stiffness(f, m_override) for f in detected_fs])
        colors_arr = np.where(new_s > 2e5, '#2196F3',
                              np.where(new_s > 8e4, '#FF9800', '#F44336'))
        ax_scatter.clear()
        ax_scatter.set_title(f'Stiffness (mass={m_override:.0f}g)')
        ax_scatter.set_xlabel('Detected Resonance Frequency (Hz)')
        ax_scatter.set_ylabel('Stiffness Index  S = f² × m^(2/3)')
        ax_scatter.grid(True, linestyle=':', alpha=0.5)
        ax_scatter.scatter(detected_fs, new_s, c=colors_arr, alpha=0.7,
                           edgecolors='k', linewidth=0.5, s=60)
        ax_scatter.axhline(y=2e5, color='#2196F3', linestyle='--', alpha=0.4)
        ax_scatter.axhline(y=8e4, color='#FF9800', linestyle='--', alpha=0.4)
        fig.canvas.draw_idle()

    mass_slider.on_changed(update)
    plt.suptitle('13주차 실습: 음향 FFT 기반 경도 지수 분석\n'
                 '(범례 텍스트 클릭 → 해당 등급 강조 / 재클릭 → 복원)',
                 fontsize=13, y=0.99)
    print("플롯 창을 확인하세요.")
    print("  ▶ 범례 텍스트(단단함/보통/물러짐)를 클릭하면 해당 데이터가 진하게 강조됩니다.")
    print("  ▶ 같은 항목을 다시 클릭하면 원래 상태로 복원됩니다.")
    print("  ▶ 하단 슬라이더로 질량 변경 시 경도 지수 재계산 결과를 실시간 확인 가능")
    plt.show()


if __name__ == '__main__':
    main()
