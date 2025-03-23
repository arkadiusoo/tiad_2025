# Excel to DOCX/PDF Converter

A simple and user-friendly desktop application for converting Excel (`.xlsx`) files to DOCX and PDF documents. Built with Python, this converter allows customization of document layout and formatting, and ensures a clean, professional look of the exported files.

## Features

- Supports Excel files with varying numbers of rows and columns
- Handles text of any length in cells (no text truncation)
- Produces aesthetically formatted DOCX and PDF documents
- Allows the user to add a document title
- Provides customization options for layout, spacing, and page numbering
- Allows saving user preferences
- Easy to use with a graphical interface
- Simple installation process

## Installation and Usage (Polish below)
### Installation
Make sure you have Python 3.8 or newer installed. Then install the required packages:

```bash
pip install -r requirements.txt
```
If requirements.txt is not provided, you can install the dependencies manually:
```bash
pip install openpyxl python-docx pandas docx2pdf
```

### Usage
Run the application from the terminal or command prompt:
```bash
python main.py
```
This will open a graphical interface where you can:

Choose an Excel file (.xlsx)
Add a document title
Customize document layout and formatting (spacing, alignment, etc.)
Export the content to a .docx and/or .pdf file

## Instalacja oraz Uruchomienie programu
### Instalacja
Upewnij się, że masz zainstalowanego Pythona w wersji 3.8 lub nowszej. Następnie zainstaluj wymagane biblioteki:
```bash
pip install -r requirements.txt
```
Jeśli nie posiadasz pliku requirements.txt, zainstaluj biblioteki ręcznie:
```bash
pip install openpyxl python-docx pandas docx2pdf
```

### Uruchomienie programu
Uruchom aplikację poleceniem:
```bash
python main.py
```
Po uruchomieniu zobaczysz graficzny interfejs, w którym możesz:

Wybrać plik Excel (.xlsx)
Dodać tytuł dokumentu
Dostosować układ i wygląd dokumentu (odstępy, wyrównanie, numerowanie stron)
Eksportować dane do pliku .docx i/lub .pdf