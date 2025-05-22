import speech_recognition
from pydub import AudioSegment

def recognize_audio(file_path, language):
    r = speech_recognition.Recognizer()
    audio = AudioSegment.from_file(file_path)
    audio.export(file_path, format="wav")

    with speech_recognition.AudioFile(file_path) as source:
        audio_data = r.record(source)
        try:
            return r.recognize_google(audio_data, language=language)
        except:
            return ""

