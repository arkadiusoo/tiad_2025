import pandas as pd
from docx import Document
import os
import subprocess

def convert_xlsx_to_docx(xlsx_path, docx_path, form, fileType):
    # Wczytanie pliku XLSX
    df = pd.read_excel(xlsx_path)
    # Tworzenie dokumentu Word
    doc = Document()
    doc.add_heading("Dane z pliku XLSX", level=1)

    if form == True:
        # Dodanie tabeli do dokumentu
        table = doc.add_table(rows=df.shape[0] + 1, cols=df.shape[1])
        table.style = 'Table Grid'
        # Dodanie nagłówków
        for j, column in enumerate(df.columns):
            table.cell(0, j).text = str(column)
        # Dodanie danych z Excela
        for i, row in df.iterrows():
            for j, value in enumerate(row):
                table.cell(i + 1, j).text = str(value)
    else:
        # Dodanie danych z Excela
        for i, row in df.iterrows():
            line_text = ""
            for value in row:
                line_text += str(value) + " "
            print(line_text)
            doc.add_paragraph(line_text.strip())
    doc.save(docx_path)
    if fileType == True:
        filename = os.path.basename(docx_path)
        #Konwersja do pdf --- nalezy tu umiescic sciezke do libre w komputerze ale mozliwe ze masz ta sama
        subprocess.run(['/Applications/LibreOffice.app/Contents/MacOS/soffice', '--headless', '--convert-to', 'pdf', filename, '--outdir', 'tmp'], check=True)
        os.rename(f'tmp/{filename.replace(".docx",".pdf")}', filename.replace(".docx",".pdf"))
        os.remove(docx_path)

