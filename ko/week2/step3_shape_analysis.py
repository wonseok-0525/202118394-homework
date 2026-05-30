import cv2
import numpy as np
import math
import os

# 앞선 step1, step2 결과 이어받기 가정
script_dir = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(script_dir, 'images', 'apple_side_A.png')
img_array = np.fromfile(image_path, np.uint8)
img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
original_display = img.copy()

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
_, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

for cnt in contours:
    area = cv2.contourArea(cnt)
    # 미세 노이즈와 눈금 제거: 너무 작거나 큰 contour 무시
    if area < 10000 or area > 1000000:
        continue
        
    perimeter = cv2.arcLength(cnt, True)
    if perimeter == 0:
        continue
        
    # A. 원형도 (Circularity) 산출
    circularity = (4 * math.pi * area) / (perimeter ** 2)
    
    # 눈금도 같은 선형 객체 제외: 원형도 0.3 이상만 (사과는 충분히 둥근 형태)
    if circularity < 0.3:
        continue
    
    # B. 구형도용 (간접 2D Bounding Box 치수 기반)
    rect = cv2.minAreaRect(cnt)
    box = cv2.boxPoints(rect)
    box = np.int32(box)
    
    dim1, dim2 = rect[1]
    pixel_L = max(dim1, dim2)
    pixel_W = min(dim1, dim2)
    
    pixel_T = 304.1
    GMD = (pixel_L * pixel_W * pixel_T) ** (1/3)
    sphericity = (GMD / pixel_L) * 100
    
    # 화면 표출 텍스트
    cv2.drawContours(original_display, [cnt], -1, (0, 255, 0), 2)
    cv2.drawContours(original_display, [box], 0, (255, 0, 0), 2)
    
    M = cv2.moments(cnt)
    if M['m00'] != 0:
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])
        
        cv2.putText(original_display, f"Circularity: {circularity:.3f}", (cx - 60, cy - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
        cv2.putText(original_display, f"Sphericity: {sphericity:.1f}%", (cx - 60, cy + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

cv2.imshow("Step 3: Final Shape Analysis", original_display)
cv2.waitKey(0)
cv2.destroyAllWindows()
