from pydub import AudioSegment
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import QThread, pyqtSignal
import speech_recognition as sr
import wave
import tempfile

def recognize_audio(file_path, language):
    r = sr.Recognizer()
    audio = AudioSegment.from_file(file_path)
    audio.export(file_path, format="wav")

    with sr.AudioFile(file_path) as source:
        audio_data = r.record(source)
        try:
            return r.recognize_google(audio_data, language=language)
        except:
            return ""



class RecordingThread(QThread):
    finished = pyqtSignal(str)

    def __init__(self, output_path):
        super().__init__()
        self.output_path = output_path
        self.running = True

    def run(self):
        recognizer = sr.Recognizer()
        mic = sr.Microphone()
        with mic as source, wave.open(self.output_path, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(16000)

            recognizer.adjust_for_ambient_noise(source)
            while self.running:
                audio = recognizer.listen(source, phrase_time_limit=1)
                wf.writeframes(audio.get_raw_data())

        self.finished.emit(self.output_path)

    def stop(self):
        self.running = False

class MicrophoneRecorderDialog(QDialog):
    recording_finished = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Recording...")
        self.setModal(True)

        self.layout = QVBoxLayout()
        self.label = QLabel("Recording... Press 'Stop' to finish.")
        self.stop_button = QPushButton("Stop")
        self.stop_button.clicked.connect(self.stop_recording)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.stop_button)
        self.setLayout(self.layout)

        self.temp_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
        self.output_path = self.temp_file.name
        self.thread = RecordingThread(self.output_path)
        self.thread.finished.connect(self.handle_finished)
        self.thread.start()

    def stop_recording(self):
        self.thread.stop()

    def handle_finished(self, path):
        self.recording_finished.emit(path)
        self.accept()
