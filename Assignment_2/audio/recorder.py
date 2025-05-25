from pydub import AudioSegment
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import QThread, pyqtSignal
import speech_recognition as sr
import wave
import tempfile
import pyaudio
import numpy as np
import pyqtgraph as pg

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
    volume_update = pyqtSignal(float)

    def __init__(self, output_path):
        super().__init__()
        self.output_path = output_path
        self.running = True

    def run(self):
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 16000

        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

        frames = []

        while self.running:
            data = stream.read(CHUNK, exception_on_overflow=False)
            frames.append(data)

            samples = np.frombuffer(data, dtype=np.int16)
            if samples.size and np.all(np.isfinite(samples)):
                rms = float(np.sqrt(np.mean(samples.astype(np.float32) ** 2)))
                self.volume_update.emit(rms)

        stream.stop_stream()
        stream.close()
        p.terminate()

        wf = wave.open(self.output_path, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()

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

        self.volume_plot = pg.PlotWidget()
        self.volume_plot.setYRange(-3000, 3000)
        self.volume_plot.setMouseEnabled(x=False, y=False)
        self.volume_plot.hideAxis('bottom')
        self.volume_plot.hideAxis('left')
        self.volume_plot.setBackground('k')
        self.volume_data = [0] * 100
        self.bar_positive = pg.BarGraphItem(x=list(range(100)), height=self.volume_data, width=0.8, brush='r')
        self.bar_negative = pg.BarGraphItem(x=list(range(100)), height=[-v for v in self.volume_data], width=0.8, brush='r')
        self.volume_plot.addItem(self.bar_positive)
        self.volume_plot.addItem(self.bar_negative)
        self.layout.addWidget(self.volume_plot)

        self.setLayout(self.layout)

        self.temp_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
        self.output_path = self.temp_file.name
        self.thread = RecordingThread(self.output_path)
        self.thread.finished.connect(self.handle_finished)
        self.thread.volume_update.connect(self.update_volume)
        self.thread.start()

    def stop_recording(self):
        self.thread.stop()

    def handle_finished(self, path):
        self.recording_finished.emit(path)
        self.accept()

    def update_volume(self, rms):
        self.volume_data = self.volume_data[1:] + [rms]
        self.bar_positive.setOpts(height=self.volume_data)
        self.bar_negative.setOpts(height=[-v for v in self.volume_data])
