import json
import cv2
from ultralytics import YOLO
import numpy as np
import math
import re
import os
from datetime import datetime
from paddleocr import PaddleOCR 
from sqldb import save_to_database  # Import hàm từ sqldb.py

# Tạo đối tượng ảnh
image = cv2.imread("data/carImage2.png")
if image is None:
    print("Không thể đọc được file ảnh!")
    exit()

# Khởi tạo mô hình YOLOv10
model = YOLO("weights/best.pt")

# Khởi tạo biến đếm khung hình
count = 0

# Tên lớp
className = ["digit"]

# Khởi tạo Paddle OCR
ocr = PaddleOCR(use_angle_cls=True, use_gpu=False)

def paddle_ocr(frame, x1, y1, x2, y2):
    frame = frame[y1:y2, x1:x2]
    result = ocr.ocr(frame, det=False, rec=True, cls=False)
    text = ""
    for r in result:
        scores = r[0][1]
        if np.isnan(scores):
            scores = 0
        else:
            scores = int(scores * 100)
        if scores > 60:
            text = r[0][0]
    pattern = re.compile('[\W]')
    text = pattern.sub('', text)
    text = text.replace("???", "")
    text = text.replace("O", "0")
    text = text.replace("粤", "")
    return str(text)

def save_json(water_meter, startTime, endTime):
    # Tạo file JSON cho mỗi khoảng thời gian
    interval_data = {
        "Start Time": startTime.isoformat(),
        "End Time": endTime.isoformat(),
        "Water Meter": list(water_meter)
    }
    interval_file_path = "json/output_" + datetime.now().strftime("%Y%m%d%H%M%S") + ".json"
    with open(interval_file_path, 'w') as f:
        json.dump(interval_data, f, indent=2)

    # File JSON tích lũy
    cummulative_file_path = "json/WT.json"
    if os.path.exists(cummulative_file_path):
        with open(cummulative_file_path, 'r') as f:
            existing_data = json.load(f)
    else:
        existing_data = []

    existing_data.append(interval_data)
    with open(cummulative_file_path, 'w') as f:
        json.dump(existing_data, f, indent=2)

    # Lưu dữ liệu vào cơ sở dữ liệu
    save_to_database(water_meter, startTime, endTime)

startTime = datetime.now()
water_meter = set()

# Xử lý ảnh đơn
frame = image
count += 1
print(f"Image Processed: {count}")
results = model.predict(frame, conf=0.45)

# Hiển thị và xử lý kết quả
for result in results: 
    boxes = result.boxes
    for box in boxes:
        x1, y1, x2, y2 = box.xyxy[0]
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
        classNameInt = int(box.cls[0])
        clsName = className[classNameInt]
        conf = math.ceil(box.conf[0] * 100) / 100
        label = paddle_ocr(frame, x1, y1, x2, y2)
        if label:
            water_meter.add(label)
        textSize = cv2.getTextSize(label, 0, fontScale=0.5, thickness=2)[0]
        c2 = x1 + textSize[0], y1 - textSize[1] - 3
        cv2.rectangle(frame, (x1, y1), c2, (255, 0, 0), -1)
        cv2.putText(frame, label, (x1, y1 - 2), 0, 0.5, [255, 255, 255], thickness=1, lineType=cv2.LINE_AA)

# Lưu kết quả
endTime = datetime.now()
save_json(water_meter, startTime, endTime)

# Hiển thị ảnh và dừng khi nhấn 'q'
cv2.imshow("Image", frame)
key = cv2.waitKey(0) & 0xFF
if key == ord('q'):
    cv2.destroyAllWindows()