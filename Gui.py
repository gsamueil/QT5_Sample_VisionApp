import sys
from PyQt5.QtWidgets import QApplication, QFileDialog, QDialog, QGraphicsScene, QPushButton
from PyQt5 import uic
from PyQt5.QtGui import QPixmap, QImage
import cv2

class ImageViewer(QDialog):
    def __init__(self) -> None:
        super(ImageViewer, self).__init__()
        # Load the UI
        uic.loadUi('new.ui', self)

        # Load QGraphicsView from UI
        self.originview = self.findChild(type(self.originview), "originview")

        # Create a QGraphicsScene to display images
        self.scene = QGraphicsScene(self)
        self.originview.setScene(self.scene)

        # Access buttons from UI
        self.button_open = self.findChild(QPushButton, "button_open")
        self.button_canny = self.findChild(QPushButton, "button_canny")
        self.button_save = self.findChild(QPushButton, "button_save")

        # Connect buttons
        self.button_open.clicked.connect(self.openFileDialog)
        self.button_canny.clicked.connect(self.applyCanny)
        self.button_save.clicked.connect(self.saveCannyImage)

        # Variables to store images
        self.img = None
        self.canny_img = None

    def openFileDialog(self):
        fileName, _ = QFileDialog.getOpenFileName(
            self, "Open Image File", "",
            "Images (*.png *.jpg *.jpeg *.bmp *.gif);;All Files (*)"
        )
        if fileName:
            self.img = cv2.imread(fileName)
            if self.img is not None:
                self.displayImage(self.img)

    def applyCanny(self):
        if self.img is not None:
            gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
            self.canny_img = cv2.Canny(gray, 100, 200)  # adjustable thresholds
            self.displayImage(self.canny_img)

    def displayImage(self, img):
        """Display image inside QGraphicsView"""
        if len(img.shape) == 2:  # grayscale
            height, width = img.shape
            qImg = QImage(img.data, width, height, width, QImage.Format_Grayscale8)
        else:
            height, width, channel = img.shape
            qImg = QImage(img.data, width, height, 3 * width, QImage.Format_RGB888).rgbSwapped()

        pixmap = QPixmap.fromImage(qImg)

        # Clear previous image
        self.scene.clear()
        self.scene.addPixmap(pixmap)

        # Fit image inside the view
        self.originview.fitInView(self.scene.items()[0], 1)

    def saveCannyImage(self):
        if self.canny_img is not None:
            save_path, _ = QFileDialog.getSaveFileName(
                self, "Save Canny Image", "canny_result.png",
                "PNG Files (*.png);;JPEG Files (*.jpg *.jpeg)"
            )
            if save_path:
                cv2.imwrite(save_path, self.canny_img)
                print(f"Canny image saved to: {save_path}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    viewer = ImageViewer()
    viewer.show()
    sys.exit(app.exec_())
