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

class WorkerSignals(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(str)
    progress = pyqtSignal(int)
    highlight = pyqtSignal(int, int)

class PDFReaderWorker(QRunnable):
    def __init__(self, engine, text, start_index):
        super().__init__()
        self.engine = engine
        self.text = text
        self.start_index = start_index
        self.signals = WorkerSignals()
        self.is_paused = False
        self.is_stopped = False

    def run(self):
        try:
            lines = self.text.split('\n')
            total_lines = len(lines)
            word_index = 0

            for i in range(self.start_index, total_lines):
                if self.is_stopped:
                    break
                
                line = lines[i].strip()
                if not line:
                    continue

                words = line.split()
                line_start_index = word_index
                
                for word in words:
                    if self.is_stopped:
                        break
                    while self.is_paused:
                        if self.is_stopped:
                            break
                    
                    self.signals.highlight.emit(word_index, len(word))
                    word_index += len(word) + 1  # +1 for space

                if not self.is_stopped and not self.is_paused:
                    self.engine.say(line)
                    self.engine.runAndWait()
                
                self.signals.progress.emit(int((i + 1) / total_lines * 100))
                word_index += 1  # +1 for newline

            self.signals.finished.emit()
        except Exception as e:
            self.signals.error.emit(str(e))

class PDFToAudioConverter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.full_text = ""
        self.current_line_index = 0
        self.engine = pyttsx3.init()
        self.reader_worker = None
        self.threadpool = QThreadPool()

    def initUI(self):
        self.setWindowTitle('PDF to Audio Converter')
        self.setGeometry(100, 100, 800, 600)

        # Set dark theme
        self.setStyleSheet("""
            QWidget {
                background-color: #2b2b2b;
                color: #00ff00;
            }
            QPushButton {
                background-color: #3b3b3b;
                color: #00ff00;
                border: 1px solid #00ff00;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #4b4b4b;
            }
            QPushButton:disabled {
                color:rgb(255, 255, 255);
                border: 1px solid rgb(255, 255, 255);
            }
            QTextEdit {
                background-color: #1b1b1b;
                color: #00ff00;
                border: 1px solid #00ff00;
            }
            QSlider::groove:horizontal {
                background: #3b3b3b;
                height: 8px;
            }
            QSlider::handle:horizontal {
                background: #00ff00;
                width: 18px;
                margin: -5px 0;
                border-radius: 9px;
            }
            QProgressBar {
                border: 1px solid rgb(255, 238, 0);
                background-color: #1b1b1b;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color:rgb(120, 42, 136);
            }
        """)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()

        # Top buttons
        top_layout = QHBoxLayout()
        self.select_button = QPushButton('Choose PDF File', self)
        self.select_button.clicked.connect(self.choose_file)
        top_layout.addWidget(self.select_button)

        self.start_button = QPushButton('Start Reading', self)
        self.start_button.clicked.connect(self.start_reading)
        top_layout.addWidget(self.start_button)

        self.pause_button = QPushButton('Pause', self)
        self.pause_button.clicked.connect(self.pause_resume_reading)
        self.pause_button.setEnabled(False)
        top_layout.addWidget(self.pause_button)

        layout.addLayout(top_layout)

        # Text area
        self.text_area = QTextEdit(self)
        self.text_area.setReadOnly(True)
        layout.addWidget(self.text_area)

        # Speed control
        speed_layout = QHBoxLayout()
        speed_label = QLabel('Speed:', self)
        speed_layout.addWidget(speed_label)
        self.speed_slider = QSlider(Qt.Horizontal, self)
        self.speed_slider.setMinimum(50)
        self.speed_slider.setMaximum(300)
        self.speed_slider.setValue(150)
        self.speed_slider.valueChanged.connect(self.change_speed)
        speed_layout.addWidget(self.speed_slider)
        self.speed_value_label = QLabel('150%', self)
        speed_layout.addWidget(self.speed_value_label)
        layout.addLayout(speed_layout)

        # Progress bar
        self.progress_bar = QProgressBar(self)
        layout.addWidget(self.progress_bar)

        central_widget.setLayout(layout)

    def choose_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Choose PDF File", "", "PDF Files (*.pdf)")
        if file_path:
            self.display_pdf(file_path)

    def display_pdf(self, file_path):
        try:
            self.text_area.clear()
            pdf_reader = PyPDF2.PdfReader(file_path)
            self.full_text = ""
            for page in pdf_reader.pages:
                self.full_text += page.extract_text() + "\n"
            self.text_area.setPlainText(self.full_text)
            self.current_line_index = 0
            self.progress_bar.setValue(0)
            
            # Reset text highlighting
            cursor = self.text_area.textCursor()
            cursor.select(QTextCursor.Document)
            format = cursor.charFormat()
            format.setBackground(Qt.transparent)
            cursor.setCharFormat(format)
            self.text_area.setTextCursor(cursor)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to read PDF: {str(e)}")

    def start_reading(self):
        if not self.full_text:
            QMessageBox.warning(self, "Warning", "Please select a PDF file first.")
            return

        self.reader_worker = PDFReaderWorker(self.engine, self.full_text, self.current_line_index)
        self.reader_worker.signals.finished.connect(self.on_reading_finished)
        self.reader_worker.signals.error.connect(self.on_reading_error)
        self.reader_worker.signals.progress.connect(self.update_progress)
        self.reader_worker.signals.highlight.connect(self.highlight_word)

        self.threadpool.start(self.reader_worker)
        
        self.start_button.setEnabled(False)
        self.pause_button.setEnabled(True)
        self.pause_button.setText("Pause")

    def pause_resume_reading(self):
        if self.reader_worker:
            if self.reader_worker.is_paused:
                self.reader_worker.is_paused = False
                self.pause_button.setText("Pause")
            else:
                self.reader_worker.is_paused = True
                self.pause_button.setText("Resume")

    def on_reading_finished(self):
        self.start_button.setEnabled(True)
        self.pause_button.setEnabled(False)
        self.progress_bar.setValue(100)

    def on_reading_error(self, error_msg):
        QMessageBox.critical(self, "Error", f"An error occurred during reading: {error_msg}")
        self.on_reading_finished()

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def change_speed(self, value):
        self.speed_value_label.setText(f'{value}%')
        self.engine.setProperty('rate', value)

    def highlight_word(self, start, length):
        # Clear previous highlighting
        cursor = self.text_area.textCursor()
        cursor.select(QTextCursor.Document)
        format = cursor.charFormat()
        format.setBackground(Qt.transparent)
        cursor.setCharFormat(format)

        # Highlight current word
        cursor.setPosition(start)
        cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor, length)

        format = cursor.charFormat()
        format.setBackground(QColor(255, 255, 255))  # Yellow highlight
        cursor.setCharFormat(format)

        self.text_area.setTextCursor(cursor)
        self.text_area.ensureCursorVisible()

    def closeEvent(self, event):
        if self.reader_worker:
            self.reader_worker.is_stopped = True
            self.reader_worker.is_paused = False
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    converter = PDFToAudioConverter()
    converter.show()
    sys.exit(app.exec_())

