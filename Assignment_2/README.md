# Voice Recipe Filter

This is a Python desktop application that allows users to filter recipes based on spoken ingredients. The user can either record an audio clip or upload an existing one. The application processes the speech, extracts recognized ingredients, and matches them with a recipe database.

## Features

- Record audio using the system microphone or upload audio files (`.wav`, `.mp3`, `.m4a`)
- Transcribe audio to text using Google Speech Recognition
- Extract known ingredients from the transcription
- Filter recipes containing any or all of the recognized ingredients
- Optional strict filtering mode: only show recipes containing all spoken ingredients
- Graphical interface with ingredient highlighting:
  - Green: present in speech
  - Red: missing from speech
- Automatic language detection using `langdetect`

## Requirements

Python 3.8 or newer is required.

### Dependencies

Install with:

```bash
pip install -r requirements.txt
```

If `requirements.txt` is not available, install manually:

```bash
pip install PyQt6 speechrecognition pyaudio pydub pyqtgraph langdetect
```

Also make sure `ffmpeg` is available in your system path:

- macOS: `brew install ffmpeg`
- Windows: install from https://ffmpeg.org/download.html

## Running the Application

Navigate to the project root and run:

```bash
python Assignment_2/main.py
```

## Building an Executable

### macOS

```bash
pyinstaller --windowed --onedir Assignment_2/main.py \
  --paths=Assignment_2 \
  --add-data "Assignment_2/data:data"
```

### Windows

```bash
pyinstaller --windowed --onefile Assignment_2/main.py ^
  --paths=Assignment_2 ^
  --add-data "Assignment_2\\data;data"
```

The final build will appear in the `dist/` directory.

## Project Structure

```
Assignment_2/
├── main.py
├── audio/
│   └── recorder.py
├── nlp/
│   └── extractor.py
├── data/
│   └── recipes.json
```

## Notes

- Ingredient matching is based on exact matches with entries in `recipes.json`.
- Only ingredients recognized by the speech recognition system and found in the recipe dataset will be considered.
- The filtering mode (any vs all ingredients) is controlled via a checkbox in the GUI.

## License

MIT License
