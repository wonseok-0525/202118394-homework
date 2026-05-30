import numpy as np
import matplotlib.pyplot as plt

# 폰트 매핑
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

fig, ax = plt.subplots(figsize=(10, 7))

# 평행판 설정
y_bottom = 0
y_top = 10
x_min = 1
x_max = 11

# 아래쪽 정지판
ax.plot([x_min, x_max], [y_bottom, y_bottom], color='black', linewidth=5)
ax.fill_between([x_min, x_max], y_bottom-1, y_bottom, color='#bbbbbb', alpha=0.5)
ax.text(x_max/2, y_bottom - 0.7, '고정판 (Stationary Plate, 속도 v=0)', fontsize=12, ha='center', fontweight='bold')

# 위쪽 이동판
ax.plot([x_min, x_max], [y_top, y_top], color='black', linewidth=5)
ax.fill_between([x_min, x_max], y_top, y_top+1, color='#add8e6', alpha=0.5)
ax.text(x_max/2, y_top + 0.4, '이동판 (Moving Plate, 단면적 Area=A)', fontsize=12, ha='center', fontweight='bold')

# 상단 판에 가해지는 힘 화살표
ax.annotate('', xy=(x_max-1, y_top), xytext=(x_min+2, y_top),
            arrowprops=dict(facecolor='red', edgecolor='red', shrink=0.05, width=3, headwidth=12))
ax.text(x_max-1.5, y_top + 0.5, '미는 힘 $F$', color='red', fontsize=14, fontweight='bold')

# 유속 속도 벡터 (Quiver) - 층류 형상
y_points = np.linspace(y_bottom, y_top, 7)
x_start = 3
for y in y_points:
    v = (y / y_top) * 5  # 최고 속도 5
    if v > 0:
        ax.annotate('', xy=(x_start + v, y), xytext=(x_start, y),
                    arrowprops=dict(facecolor='blue', edgecolor='blue', shrink=0, width=2, headwidth=8))

# 유체 층 간 속도 프로파일 (점선)
ax.plot([x_start, x_start+5], [y_bottom, y_top], 'b--', alpha=0.6, linewidth=2)

# 치수선 및 개념 표기
# dy 표기
ax.annotate('', xy=(x_start-0.5, y_top), xytext=(x_start-0.5, y_bottom),
            arrowprops=dict(arrowstyle='<->', color='black', lw=1.5))
ax.text(x_start-0.8, y_top/2, '수직 거리 $dy$', fontsize=12, va='center', rotation=90)

# dv 표기
ax.text(x_start+5.3, y_top-0.5, '최고 유속 $dv$', fontsize=12, color='blue', fontweight='bold')

# 메인 공식 해설 박스
bbox_props = dict(boxstyle="round,pad=0.5", fc="white", ec="gray", alpha=0.9, lw=1.5)
ax.text(7.5, 6, 
        "1. 전단 응력 (Shear Stress, $\\tau$)\n"
        "   $\\rightarrow \\tau = \\frac{F}{A}$ (단위: $Pa$)\n"
        "   (면적 A당 가해지는 힘)\n\n"
        "2. 전단 속도 (Shear Rate, $\\dot{\\gamma}$)\n"
        "   $\\rightarrow \\dot{\\gamma} = \\frac{dv}{dy}$ (단위: $s^{-1}$)\n"
        "   (간격 $dy$에 따른 속도 $dv$의 기울기)", 
        fontsize=13, bbox=bbox_props)

ax.set_xlim(0, 14)
ax.set_ylim(-2, 12)
ax.axis('off')
ax.set_title('유변학 기초: 전단 응력과 전단 속도의 개념 (뉴턴의 평행판 모델)', fontsize=16, fontweight='bold', pad=20)

plt.tight_layout()
plt.show()
