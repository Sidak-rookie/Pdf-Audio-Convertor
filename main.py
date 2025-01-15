import sys
from PyQt5.QtWidgets import QApplication
from pdf_to_aud import PDFToAudioConverter

if __name__ == '__main__':
    app = QApplication(sys.argv)  # Create an instance of QApplication
    converter = PDFToAudioConverter()  # Create an instance of the main window
    converter.show()  # Show the main window
    sys.exit(app.exec_())  # Execute the application
