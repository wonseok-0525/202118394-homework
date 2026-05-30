import cv2
import numpy as np
import os

def main():
    # 1. 이미지 로드
    # 현재 스크립트 경로를 기준으로 이미지 경로 설정
    base_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(base_dir, 'images', 'sample_tomatoes.png')
    
    # 이미지 읽기 (한글 경로 지원을 위해 numpy와 imdecode 사용)
    img_array = np.fromfile(image_path, np.uint8)
    image_bgr = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    
    if image_bgr is None:
        print(f"오류: 이미지를 찾을 수 없습니다. 경로를 확인하세요: {image_path}")
        return

    # 크기 조절 (병합 화면에 잘 보이도록 400x300으로 축소)
    image_bgr = cv2.resize(image_bgr, (400, 300))
    
    # 2. 색좌표계 변환 (BGR -> HSV, BGR -> CIE Lab)
    image_hsv = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV)
    image_lab = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2LAB)

    # 3. HSV 색 공간을 이용한 적색(Red) 마스킹
    # OpenCV에서 Hue(H)는 0~179 범위. 빨간색은 0 부근과 179 부근 양쪽에 분포함.
    # Lower Red 범위 (0~10)
    lower_red1 = np.array([0, 70, 50])
    upper_red1 = np.array([10, 255, 255])
    # Upper Red 범위 (170~179)
    lower_red2 = np.array([170, 70, 50])
    upper_red2 = np.array([179, 255, 255])

    mask_hsv1 = cv2.inRange(image_hsv, lower_red1, upper_red1)
    mask_hsv2 = cv2.inRange(image_hsv, lower_red2, upper_red2)
    mask_hsv_final = cv2.bitwise_or(mask_hsv1, mask_hsv2)

    # 마스크를 원본 이미지에 적용
    result_hsv = cv2.bitwise_and(image_bgr, image_bgr, mask=mask_hsv_final)

    # 4. CIE Lab 색 공간을 이용한 적색(Red) 마스킹
    # OpenCV에서 L(0~255), a(0~255), b(0~255). a채널이 높을수록 Red 특성이 강함.
    # L: 20~255, a: 150~255 (Red 영역), b: 0~255
    lower_lab = np.array([20, 140, 100])
    upper_lab = np.array([255, 255, 255])

    mask_lab = cv2.inRange(image_lab, lower_lab, upper_lab)
    
    # 마스크를 원본 이미지에 적용
    result_lab = cv2.bitwise_and(image_bgr, image_bgr, mask=mask_lab)
    
    # 5. 결과 저장 (한글 경로 지원을 위해 imencode 사용)
    hsv_path = os.path.join(base_dir, 'images', 'result_hsv.png')
    lab_path = os.path.join(base_dir, 'images', 'result_lab.png')
    
    cv2.imencode('.png', result_hsv)[1].tofile(hsv_path)
    cv2.imencode('.png', result_lab)[1].tofile(lab_path)
    print("결과가 images 폴더에 저장되었습니다.")

    # 6. 결과 화면 출력 (비교하기 쉽게 하나의 창으로 병합)
    # 흑백 마스크 이미지를 컬러 이미지와 병합하기 위해 3채널로 변환
    mask_hsv_3c = cv2.cvtColor(mask_hsv_final, cv2.COLOR_GRAY2BGR)
    mask_lab_3c = cv2.cvtColor(mask_lab, cv2.COLOR_GRAY2BGR)

    # 텍스트 추가 함수
    def add_text(img, text):
        img_copy = img.copy()
        cv2.putText(img_copy, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2, cv2.LINE_AA)
        return img_copy

    # 각 이미지에 라벨 추가
    img_orig = add_text(image_bgr, "Original")
    img_hsv_mask = add_text(mask_hsv_3c, "HSV Mask")
    img_hsv_res = add_text(result_hsv, "HSV Result")
    img_lab_mask = add_text(mask_lab_3c, "Lab Mask")
    img_lab_res = add_text(result_lab, "Lab Result")

    # 2x3 그리드로 이미지 병합
    row1 = np.hstack([img_orig, img_hsv_mask, img_hsv_res])
    row2 = np.hstack([img_orig, img_lab_mask, img_lab_res])
    combined_image = np.vstack([row1, row2])

    cv2.imshow('Color Sorting Comparison', combined_image)

    print("화면에 뜬 팝업 창(OpenCV)을 확인하세요. (혹시 안 보이면 작업 표시줄의 Python 아이콘을 클릭하세요.)")
    print("팝업 창이 선택된 상태에서 아무 키나 누르면 종료됩니다.")
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
