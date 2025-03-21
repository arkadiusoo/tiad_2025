import pandas as pd
from docx import Document
import os
import subprocess

def convert_xlsx_to_docx(xlsx_path, docx_path, form, fileType):
    fileExcel = os.path.basename(xlsx_path)
    fileExcel = os.path.splitext(fileExcel)[0]
    # Wczytanie pliku XLSX
    df = pd.read_excel(xlsx_path)
    # Tworzenie dokumentu Word
    doc = Document()
    doc.add_heading(fileExcel, level=1)

    columns_per_table = 10

    if form == True:
        if df.shape[1] > 10:
            for start_col in range(0, df.shape[1], columns_per_table):
                end_col = min(start_col + columns_per_table, df.shape[1])
                sub_df = df.iloc[:, start_col:end_col]

                table = doc.add_table(rows=sub_df.shape[0] + 1, cols=sub_df.shape[1])
                table.style = 'Table Grid'

                for j, column in enumerate(sub_df.columns):
                    table.cell(0, j).text = str(column)

                for i, row in sub_df.iterrows():
                    for j, value in enumerate(row):
                        table.cell(i + 1, j).text = str(value)

                doc.add_paragraph("")
        else:
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
        header = ""
        for j, column in enumerate(df.columns):
            header += str(column) + " "
        doc.add_paragraph(header.strip())
        for i, row in df.iterrows():
            line_text = ""
            for value in row:
                line_text += str(value) + " "
            doc.add_paragraph(line_text.strip())
    doc.save(docx_path)
    if fileType == True:
        filename = os.path.basename(docx_path)
        #Konwersja do pdf --- nalezy tu umiescic sciezke do libre w komputerze ale mozliwe ze masz ta sama
        subprocess.run(['/Applications/LibreOffice.app/Contents/MacOS/soffice', '--headless', '--convert-to', 'pdf', filename, '--outdir', 'tmp'], check=True)
        os.rename(f'tmp/{filename.replace(".docx",".pdf")}', filename.replace(".docx",".pdf"))
        os.remove(docx_path)



