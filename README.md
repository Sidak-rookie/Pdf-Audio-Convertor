# PDF to Audio Converter - README

## 🎉 Welcome to the PDF to Audio Converter! 🎉

This project is a Python application that transforms PDF documents into spoken audio, making it easier for users to consume written content. Whether you're a student, a professional, or someone who enjoys listening to books, this tool is designed for you! 📚➡️🔊

---

## 🚀 Features

- **User-Friendly Interface**: Built with PyQt5, the application offers an intuitive GUI that allows users to easily navigate and operate the converter.
- **Text-to-Speech Conversion**: Utilizes the `pyttsx3` library to convert text from PDFs into speech, enabling auditory learning.
- **Playback Controls**: Start, pause, and resume audio playback with simple button clicks, giving you complete control over your listening experience.
- **Adjustable Speed**: Customize the reading speed according to your preference using a slider.
- **Progress Tracking**: A progress bar visually indicates how much of the document has been read, enhancing user engagement.
- **Highlighting Feature**: As the text is read aloud, the current word is highlighted in real-time for better tracking.

---

## 📦 Installation

To get started with the PDF to Audio Converter, follow these steps:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Sidak-rookie/pdf-to-audio-converter.git
   ```
2. **Navigate to the Project Directory**:
   ```bash
   cd pdf-to-audio-converter
   ```
3. **Install Required Libraries**:
   Make sure you have Python installed, then run:
   ```bash
   pip install PyPDF2 pyttsx3 PyQt5
   ```

---

## 🎨 User Interface Overview

The application features a dark-themed interface that is easy on the eyes. Here’s what you can expect:

- **Choose PDF File Button**: Click this button to select a PDF file from your computer.
- **Start Reading Button**: Initiates the text-to-speech conversion and starts reading the selected PDF.
- **Pause Button**: Allows you to pause or resume reading at any time.
- **Speed Control Slider**: Adjusts the reading speed from 50% to 300%.
- **Progress Bar**: Displays the current progress of the audio playback.

---

## 🛠️ How to Use

1. **Launch the Application**:
   Run the application using:
   ```bash
   python pdf_to_aud.py
   ```
2. **Select a PDF File**:
   Click on "Choose PDF File" and navigate to your desired document.
3. **Start Listening**:
   Hit "Start Reading" to begin the audio playback of your PDF document.
4. **Control Playback**:
   Use the "Pause" button to pause or resume as needed.

---

## ⚙️ Code Structure

The core functionality of this application is structured into several classes:

- **PDFToAudioConverter**: The main window that initializes and manages UI components.
- **PDFReaderWorker**: A worker class that handles text extraction and speech synthesis in a separate thread for smooth operation.
- **WorkerSignals**: A class that manages signals for communication between threads.

### Example Code Snippet
Here’s a brief look at how we initialize our text-to-speech engine:

```python
self.engine = pyttsx3.init()
self.engine.setProperty('rate', 150)  # Set default speed
```

---

## 📄 License

This project is licensed under the MIT License. Feel free to use, modify, and distribute it as per your requirements.

---

## 🤝 Contributing

We welcome contributions! If you want to enhance this project or fix bugs, please fork the repository and submit a pull request. Your input is invaluable! 💡

---

## 📞 Contact

For any queries or feedback, feel free to reach out via GitHub issues or contact me directly at [sharsidak@gmail.com].

---

## 🎊 Thank You for Using PDF to Audio Converter! 🎊

We hope this tool makes your reading experience more enjoyable and accessible. Happy listening! 🎧

Citations:
[1] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/49164633/ad155a11-0d5c-4ef7-b45f-f9ee6d9dd61a/pdf_to_aud.py
