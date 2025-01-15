import sys
import os
import PyPDF2
import pyttsx3
import threading
import re
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QTextEdit, QFileDialog, QSlider, QLabel, 
                             QProgressBar, QMessageBox)
from PyQt5.QtCore import Qt, QUrl, pyqtSignal, QObject, QRunnable, QThreadPool
from PyQt5.QtGui import QFont, QTextCursor, QPalette, QColor
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent


if __name__ == '__main__':
    app = QApplication(sys.argv)
    converter = PDFToAudioConverter()
    converter.show()
    sys.exit(app.exec_())

