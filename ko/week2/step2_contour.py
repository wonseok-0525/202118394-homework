import cv2
import numpy as np
import os

# step1 작업 결과 이어받기 가정
script_dir = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(script_dir, 'images', 'apple_side_A.png')
img_array = np.fromfile(image_path, np.uint8)
img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
original_display = img.copy()

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# 3. 이진화 (Otsu's Thresholding)
_, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

# 4. 윤곽선 추출 (Contour)
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# 5. 윤곽선 시각화
for cnt in contours:
    area = cv2.contourArea(cnt)
    # 미세 노이즈 윤곽선 제거
    if area < 500:
        continue
    # 타겟 사과 초록색 윤곽선 표시
    cv2.drawContours(original_display, [cnt], -1, (0, 255, 0), 2)

cv2.imshow("Step 2: Threshold & Contour", original_display)
cv2.waitKey(0)
cv2.destroyAllWindows()
