import sys #  Import โมดูล sys เพื่อใช้ในการจัดการพารามิเตอร์ของคำสั่งเริ่มต้น.
import cv2 #  Import OpenCV เพื่อใช้ในการจัดการกับกล้องเว็บแคมและการประมวลผลภาพใบหน้า.
from PyQt5.QtCore import QTimer # จาก PyQt5 เพื่อใช้ในการสร้างตัวจับเวลาสำหรับอัปเดตภาพ.
from PyQt5.QtGui import QImage, QPixmap # พื่อใช้ในการแสดงภาพ.
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QVBoxLayout, QWidget # Import คลาสและองค์ประกอบที่จำเป็นจาก PyQt5 สำหรับการสร้าง GUI.

class FaceDetectionApp(QMainWindow): # สร้างคลาส FaceDetectionApp ที่สืบทอดมาจาก QMainWindow เพื่อสร้างหน้าต่าง GUI หลักของแอปพลิเคชัน
    def __init__(self): # เริ่มเมท็อดคอนสตรักเตอร์สำหรับคลาส FaceDetectionApp.
        super().__init__() # รียกเมท็อดคอนสตรักเตอร์ของ QMainWindow เพื่อกำหนดค่าเริ่มต้นของหน้าต่าง.

        self.setWindowTitle("Face Detection") # สร้างหน้าต่าง GUI, ลิมิตขนาด, และสร้าง widget หลักของแอปพลิเคชัน.
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget() 
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.video_label = QLabel(self)
        self.layout.addWidget(self.video_label)

        self.video_capture = cv2.VideoCapture(0)
        self.timer = QTimer(self) 
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(10) # เปิดการเชื่อมต่อกับกล้องเว็บแคม และตั้งค่า QTimer สำหรับอัพเดตภาพทุก 10 มิลลิวินาที.
 
    def update_frame(self): #  เมท็อดที่ใช้ในการอัปเดตภาพจากกล้องเว็บแคมและแสดงภาพที่ได้.
        ret, frame = self.video_capture.read()
        if ret:
            # ทำการตรวจจับใบหน้าด้วย OpenCV
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            # วาดสี่เหลี่ยมรอบใบหน้า
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

            # แก้ไขสมดุลสีในภาพ
            balanced_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # เปลี่ยนสีภาพให้สมดุล

            # แสดงภาพจากกล้องในหน้าต่าง PyQt5
            height, width, channel = balanced_frame.shape
            bytes_per_line = 3 * width
            qt_image = QImage(balanced_frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qt_image)
            self.video_label.setPixmap(pixmap)

    def closeEvent(self, event): # เมท็อดที่ใช้ในปิดการเชื่อมต่อกับกล้องเว็บแคมเมื่อปิดโปรแกรม.
        self.video_capture.release()

def main():  # : เริ่มเมท็อด main สำหรับการเริ่มต้นแอปพลิเคชัน.
    app = QApplication(sys.argv)
    window = FaceDetectionApp() # สร้างแอปพลิเคชัน PyQt5 และหน้าต่างหลักของแอปพลิเคชัน (FaceDetectionApp).
    window.show()  # แสดงหน้าต่าง GUI และเริ่มทำงาน.
    sys.exit(app.exec_())

if __name__ == "__main__": # เช็คว่าไฟล์ถูกเรียกโดยตรงหรือไม่.
    main() # เรียกเมท็อด main เพื่อเริ่มต้นแอปพลิเคชัน.
