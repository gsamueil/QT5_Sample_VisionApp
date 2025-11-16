import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QFileDialog
from PyQt5.QtGui import QPixmap, QImage
from PyQt5 import uic , Qt , QtWidgets
import cv2
import numpy as np

class ImageViewer(QtWidgets.QDialog):
    def __init__(self):
        super().__init__() 
        # self.initUI()
    
    # def initUI(self):
        uic.loadUi('new.ui', self)

        self.image_label_origin = QLabel(self)
        self.image_label_mediian = QLabel(self)
        self.image_label_otssus = QLabel(self)
        self.image_label_cannny = QLabel(self)
        self.image_label_hariiis = QLabel(self)
        self.image_label_sifftt = QLabel(self)

        
        self.button_open.clicked.connect(self.openFileDialog)
    
        
        # self.button_canny.clicked.connect(self.applyCanny)
        
        # self.button_median.clicked.connect(self.applyMedian)
        
        # self.button_otsu.clicked.connect(self.applyOtsu)
        
        # self.button_harris.clicked.connect(self.applyHarris)
        
        # self.button_sift.clicked.connect(self.app)

        self.img = None
    
    def openFileDialog(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Image File", "",
                                                  "Images (*.png *.xpm *.jpg *.jpeg *.bmp *.gif);;All Files (*)", options=options)
        if fileName:
            self.img = cv2.imread(fileName)
            self.displayImage(self.img, self.image_label_original)
    
    def displayImage(self, img, label):
        height, width, channel = img.shape
        bytesPerLine = 3 * width
        qImg = QImage(img.data, width, height, bytesPerLine, QImage.Format_RGB888).rgbSwapped()
        label.setPixmap(QPixmap.fromImage(qImg))
    
    def applyCanny(self):
        if self.img is not None:
            img_median = cv2.medianBlur(self.img, 5)
            img_canny = cv2.Canny(img_median, 100, 200)
            img_canny_colored = cv2.cvtColor(img_canny, cv2.COLOR_GRAY2BGR)
            self.displayImage(img_canny_colored, self.image_label_processed)
    
    def applyMedian(self):
        if self.img is not None:
            img_median = cv2.medianBlur(self.img, 5)
            self.displayImage(img_median, self.image_label_processed)
    
    def applyOtsu(self):
        if self.img is not None:
            gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
            _, img_otsu = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            img_otsu_colored = cv2.cvtColor(img_otsu, cv2.COLOR_GRAY2BGR)
            self.displayImage(img_otsu_colored, self.image_label_processed)
    
    def applyHarris(self):
        if self.img is not None:
            gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
            gray = np.float32(gray)
            dst = cv2.cornerHarris(gray, 2, 3, 0.04)
            dst = cv2.dilate(dst, None)
            img_harris = self.img.copy()
            img_harris[dst > 0.01 * dst.max()] = [0, 0, 255]
            self.displayImage(img_harris, self.image_label_processed)
    
    def applySift(self):
        if self.img is not None:
            gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
            sift = cv2.SIFT_create()
            keypoints, descriptors = sift.detectAndCompute(gray, None)
            img_sift = cv2.drawKeypoints(self.img, keypoints, None)
            self.displayImage(img_sift, self.image_label_processed)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    viewer = ImageViewer()
    viewer.show()
    sys.exit(app.exec_())
