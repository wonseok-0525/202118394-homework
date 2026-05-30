import cv2
import numpy as np
import os

# 1. 영상 로드 (한글 경로 지원을 위해 imdecode 사용 권장)
script_dir = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(script_dir, 'images', 'apple_side_A.png')
img_array = np.fromfile(image_path, np.uint8)
img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

if img is None:
    print("Error: 이미지를 찾을 수 없습니다.")
    exit()

# 2. 전처리 (그레이스케일 및 Gaussian Blur)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# 중간 결과 확인 (키 입력 시 다음 창으로)
cv2.imshow("Step 1: Original Image", img)
cv2.waitKey(0)
cv2.imshow("Step 1: Grayscale", gray)
cv2.waitKey(0)
cv2.imshow("Step 1: Blurred", blurred)
cv2.waitKey(0)
cv2.destroyAllWindows()
