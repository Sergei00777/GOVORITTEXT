import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget,
                             QLabel, QTextEdit, QPushButton, QComboBox,
                             QHBoxLayout, QFileDialog, QMessageBox)
from PyQt5.QtCore import Qt
import pyttsx3
from gtts import gTTS
import os


class TextToSpeechApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Текст в речь")
        self.setGeometry(100, 100, 600, 500)

        self.init_ui()

    def init_ui(self):
        # Главный виджет и layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()

        # Заголовок
        title_label = QLabel("Текст в речь (TTS)")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 15px;")
        layout.addWidget(title_label)

        # Поле для ввода текста
        self.text_input = QTextEdit()
        self.text_input.setPlaceholderText("Введите текст для озвучивания...")
        self.text_input.setStyleSheet("font-size: 14px; min-height: 150px;")
        layout.addWidget(self.text_input)

        # Выбор языка (для gTTS)
        self.lang_label = QLabel("Язык (gTTS):")
        self.lang_combo = QComboBox()
        self.lang_combo.addItems(["Русский", "Английский", "Немецкий", "Французский"])
        self.lang_combo.setCurrentIndex(0)

        # Выбор голоса (для pyttsx3)
        self.voice_label = QLabel("Голос (pyttsx3):")
        self.voice_combo = QComboBox()
        self.voice_combo.addItems(["Мужской", "Женский"])

        # Расположение ComboBox в одной строке
        hbox = QHBoxLayout()
        hbox.addWidget(self.lang_label)
        hbox.addWidget(self.lang_combo)
        hbox.addWidget(self.voice_label)
        hbox.addWidget(self.voice_combo)
        layout.addLayout(hbox)

        # Кнопка выбора папки для сохранения
        self.save_btn = QPushButton("Выбрать папку для сохранения")
        self.save_btn.clicked.connect(self.choose_directory)
        self.save_btn.setStyleSheet("background-color: #FF9800; color: white;")

        # Текущая папка для сохранения
        self.save_path_label = QLabel("Папка: " + os.getcwd())
        self.save_path_label.setStyleSheet("font-size: 12px; color: #555;")

        layout.addWidget(self.save_btn)
        layout.addWidget(self.save_path_label)

        # Кнопки для озвучивания
        buttons_layout = QHBoxLayout()

        self.online_btn = QPushButton("Озвучить (gTTS - онлайн)")
        self.online_btn.clicked.connect(self.speak_online)
        self.online_btn.setStyleSheet("background-color: #4CAF50; color: white;")

        self.offline_btn = QPushButton("Озвучить (pyttsx3 - оффлайн)")
        self.offline_btn.clicked.connect(self.speak_offline)
        self.offline_btn.setStyleSheet("background-color: #2196F3; color: white;")

        buttons_layout.addWidget(self.online_btn)
        buttons_layout.addWidget(self.offline_btn)
        layout.addLayout(buttons_layout)

        central_widget.setLayout(layout)

        # Переменная для хранения пути сохранения
        self.save_dir = os.getcwd()

    def choose_directory(self):
        """Выбор папки для сохранения аудио"""
        directory = QFileDialog.getExistingDirectory(self, "Выберите папку")
        if directory:
            self.save_dir = directory
            self.save_path_label.setText("Папка: " + directory)

    def speak_online(self):
        """Озвучивание через gTTS (онлайн)"""
        text = self.text_input.toPlainText().strip()
        if not text:
            self.show_warning("Введите текст для озвучивания!")
            return

        try:
            # Определяем язык
            lang_map = {
                "Русский": "ru",
                "Английский": "en",
                "Немецкий": "de",
                "Французский": "fr"
            }
            lang = lang_map[self.lang_combo.currentText()]

            tts = gTTS(text=text, lang=lang)
            filename = os.path.join(self.save_dir, "tts_output.mp3")
            tts.save(filename)

            # Проигрываем файл
            if sys.platform == "win32":
                os.startfile(filename)
            else:
                os.system(f"xdg-open {filename}")

            self.show_info("Аудиофайл сохранен и воспроизводится!")
        except Exception as e:
            self.show_error(f"Ошибка: {e}")

    def speak_offline(self):
        """Озвучивание через pyttsx3 (оффлайн)"""
        text = self.text_input.toPlainText().strip()
        if not text:
            self.show_warning("Введите текст для озвучивания!")
            return

        try:
            engine = pyttsx3.init()

            # Настройки голоса
            voices = engine.getProperty('voices')
            if self.voice_combo.currentText() == "Мужской" and len(voices) > 0:
                engine.setProperty('voice', voices[0].id)  # Первый голос (обычно мужской)
            elif len(voices) > 1:
                engine.setProperty('voice', voices[1].id)  # Второй голос (женский)

            engine.setProperty('rate', 150)  # Скорость речи
            engine.setProperty('volume', 1.0)  # Громкость

            engine.say(text)
            engine.runAndWait()
        except Exception as e:
            self.show_error(f"Ошибка: {e}")

    def show_warning(self, message):
        """Показать предупреждение"""
        QMessageBox.warning(self, "Внимание", message)

    def show_error(self, message):
        """Показать ошибку"""
        QMessageBox.critical(self, "Ошибка", message)

    def show_info(self, message):
        """Показать информационное сообщение"""
        QMessageBox.information(self, "Успех", message)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TextToSpeechApp()
    window.show()
    sys.exit(app.exec_())