import cv2

# โหลดรูปภาพ
image = cv2.imread('people.jpg')

# แปลงรูปภาพให้อยู่ในรูปแบบ grayscale
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# ใช้ Haar Cascade Classifier สำหรับตรวจจับหน้าคน
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# ทำการตรวจจับหน้าคนในรูปภาพ
# ปรับค่า scaleFactor, minNeighbors, และ minSize ตามความเหมาะสม
faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

# วาดสี่เหลี่ยมรอบหน้าคนที่ตรวจพบบนรูปภาพ
for (x, y, w, h) in faces:
    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    # นับจำนวนหน้าคนที่ตรวจพบ
num_people = len(faces)

# แสดงจำนวนคนในรูปภาพ
print(f'จำนวนคนในรูป: {num_people}')

# บันทึกรูปภาพที่มีสี่เหลี่ยมรอบหน้าคนไปยังไฟล์ภาพใหม่
cv2.imwrite('detected_people.jpg', image)

# ปิดหน้าต่างแสดงรูปภาพ (ถ้ามี)
cv2.destroyAllWindows()
