"""
avocado_profile.py — 아보카도 레퍼런스 이미지에서 프로파일 데이터 자동 추출
=============================================================================
OpenCV를 사용하여 avocado_front_view.png에서 윤곽선을 검출하고,
길이 방향 반지름 프로파일을 추출합니다.

의존성: pip install opencv-python numpy scipy
"""
import cv2
import numpy as np
import os


# 교재 예제 3-3 기준 아보카도 전체 길이 [cm]
AVOCADO_LENGTH_CM = 10.85


def _imread_unicode(filepath):
    """
    한글 등 유니코드 경로에서도 이미지를 로드할 수 있는 함수.
    cv2.imread()는 Windows에서 비-ASCII 경로를 지원하지 않으므로,
    numpy + cv2.imdecode 조합으로 우회합니다.
    """
    try:
        with open(filepath, 'rb') as f:
            buf = np.frombuffer(f.read(), dtype=np.uint8)
        img = cv2.imdecode(buf, cv2.IMREAD_COLOR)
        return img
    except Exception:
        return None


def extract_profile(image_path=None, n_dense=200):
    """
    아보카도 이미지를 로드하고 윤곽선 기반 프로파일 데이터를 추출합니다.

    Parameters
    ----------
    image_path : str, optional
        이미지 파일 경로. None이면 images/avocado_front_view.png 자동 탐색
    n_dense : int
        조밀 프로파일 샘플 수 (기본 200)

    Returns
    -------
    dict
        x_points, r_points   : 스플라인 보간용 포인트 (~15개, 양 끝 보강)
        x_textbook, r_textbook : 교재 위치 기준 측정 포인트 (6개)
        x_dense, r_dense     : 조밀 프로파일 (n_dense개)
        image                 : 원본 이미지 (BGR)
        contour               : 검출된 아보카도 윤곽선
        scale                 : 픽셀→cm 변환 계수
        from_image            : 이미지 처리 성공 여부
    """
    # --- 이미지 경로 결정 ---
    if image_path is None:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(script_dir, 'images', 'avocado_front_view.png')

    image = _imread_unicode(image_path)
    if image is None:
        print(f"[경고] 이미지를 찾을 수 없습니다: {image_path}")
        print("[대체] 교재 예제 3-3 데이터를 사용합니다.")
        return _fallback_data()

    print(f"[INFO] 이미지 로드 완료: {image_path}")
    print(f"       크기: {image.shape[1]} x {image.shape[0]} px")

    try:
        result = _process_image(image, n_dense)
        print(f"[INFO] 프로파일 추출 성공 -- 길이: {result['x_points'][-1]:.2f} cm, "
              f"최대 반지름: {result['r_points'].max():.3f} cm")
        return result
    except Exception as e:
        print(f"[경고] 이미지 처리 실패 ({e})")
        print("[대체] 교재 예제 3-3 데이터를 사용합니다.")
        return _fallback_data()


def _process_image(image, n_dense):
    """OpenCV 기반 이미지 처리 파이프라인."""
    h_img, w_img = image.shape[:2]

    # 1) 그레이스케일 변환 + 가우시안 블러
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (7, 7), 0)

    # 2) Otsu 이진화 (밝은 배경 → 반전)
    _, binary = cv2.threshold(blurred, 0, 255,
                              cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # 3) 모폴로지 연산: 노이즈 제거 및 객체 연결
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))
    binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel, iterations=3)
    binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel, iterations=2)

    # 4) 윤곽선 검출
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL,
                                   cv2.CHAIN_APPROX_NONE)

    # 면적 기준 필터링 (전체 이미지의 1% 이상인 윤곽선만)
    min_area = h_img * w_img * 0.01
    valid = [c for c in contours if cv2.contourArea(c) > min_area]
    if not valid:
        raise ValueError("유효한 윤곽선을 찾을 수 없음")

    # 가장 큰 윤곽선 = 아보카도
    avocado = max(valid, key=cv2.contourArea)
    bx, by, bw, bh = cv2.boundingRect(avocado)
    pts = avocado.reshape(-1, 2)

    # 5) 방향 판별 및 스케일 계산
    if bh >= bw:
        # 세로 방향 (길이축 = Y)
        length_px = bh
        scale = AVOCADO_LENGTH_CM / length_px
        positions = np.linspace(by, by + bh, n_dense)
        radii_px = _extract_widths(pts, positions, axis='y',
                                   tol=max(3, bh * 0.015))
        x_cm = (positions - by) * scale
    else:
        # 가로 방향 (길이축 = X)
        length_px = bw
        scale = AVOCADO_LENGTH_CM / length_px
        positions = np.linspace(bx, bx + bw, n_dense)
        radii_px = _extract_widths(pts, positions, axis='x',
                                   tol=max(3, bw * 0.015))
        x_cm = (positions - bx) * scale

    r_cm = np.array(radii_px) * scale

    # 6) 스무딩 + 보정
    from scipy.ndimage import uniform_filter1d
    r_cm = uniform_filter1d(r_cm, size=9)
    r_cm = np.maximum(r_cm, 0)
    r_cm[0] = 0
    r_cm[-1] = 0

    # 7) 교재 측정 위치에 대응하는 6개 핵심 포인트 샘플링
    textbook_ratios = np.array([0, 1.0, 5.0, 6.5, 8.0, 10.85]) / AVOCADO_LENGTH_CM
    textbook_x = textbook_ratios * x_cm[-1]
    textbook_r = np.interp(textbook_x, x_cm, r_cm)
    textbook_r[0] = 0
    textbook_r[-1] = 0

    # 8) 스플라인 보간용 포인트: 균등 간격 + 양 끝 보강
    #    6개만 사용하면 간격이 넓어 스플라인 오버슈트 발생하므로
    #    충분한 포인트를 제공합니다.
    n_spline = 15
    spline_x = np.linspace(0, x_cm[-1], n_spline)
    # 양 끝 근처에 추가 포인트 삽입 (테이퍼링 보강)
    extra_near_start = np.array([x_cm[-1] * 0.02, x_cm[-1] * 0.05])
    extra_near_end = np.array([x_cm[-1] * 0.95, x_cm[-1] * 0.98])
    spline_x = np.unique(np.sort(np.concatenate([spline_x, extra_near_start, extra_near_end])))
    spline_r = np.interp(spline_x, x_cm, r_cm)
    spline_r[0] = 0
    spline_r[-1] = 0

    return {
        'x_points': spline_x,
        'r_points': spline_r,
        'x_textbook': textbook_x,
        'r_textbook': textbook_r,
        'x_dense': x_cm,
        'r_dense': r_cm,
        'image': image,
        'contour': avocado,
        'binary': binary,
        'scale': scale,
        'bbox': (bx, by, bw, bh),
        'from_image': True,
    }


def _extract_widths(pts, positions, axis, tol):
    """윤곽선 점들로부터 각 위치에서의 폭(직경의 절반)을 추출."""
    radii = []
    for pos in positions:
        if axis == 'y':
            mask = np.abs(pts[:, 1] - pos) < tol
            nearby = pts[mask]
            if len(nearby) >= 2:
                radii.append((nearby[:, 0].max() - nearby[:, 0].min()) / 2.0)
            else:
                radii.append(0)
        else:  # axis == 'x'
            mask = np.abs(pts[:, 0] - pos) < tol
            nearby = pts[mask]
            if len(nearby) >= 2:
                radii.append((nearby[:, 1].max() - nearby[:, 1].min()) / 2.0)
            else:
                radii.append(0)
    return radii


def _fallback_data():
    """교재 예제 3-3 하드코딩 데이터 (이미지 미사용 시)."""
    x = np.array([0, 1.0, 5.0, 6.5, 8.0, 10.85])
    r = np.array([0, 1.47, 3.185, 3.38, 3.04, 0])
    return {
        'x_points': x,
        'r_points': r,
        'x_textbook': x.copy(),
        'r_textbook': r.copy(),
        'x_dense': None,
        'r_dense': None,
        'image': None,
        'contour': None,
        'binary': None,
        'scale': None,
        'bbox': None,
        'from_image': False,
    }


# === 직접 실행 시 테스트 ===
if __name__ == '__main__':
    data = extract_profile()
    print("\n=== 추출된 측정 포인트 ===")
    print(f"{'위치 x [cm]':>12} | {'반지름 r [cm]':>14}")
    print("-" * 30)
    for x, r in zip(data['x_points'], data['r_points']):
        print(f"{x:>12.3f} | {r:>14.3f}")
    print(f"\n이미지 기반: {'예' if data['from_image'] else '아니오 (교재 데이터)'}")
