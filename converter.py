import pandas as pd
from docx import Document


def convert_xlsx_to_docx(xlsx_path, docx_path):
    # Wczytanie pliku XLSX
    df = pd.read_excel(xlsx_path)

    # Tworzenie dokumentu Word
    doc = Document()
    doc.add_heading("Dane z pliku XLSX", level=1)

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

    # Zapisanie dokumentu DOCX
    doc.save(docx_path)
