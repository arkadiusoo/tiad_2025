import pandas as pd
from docx import Document
from docx.shared import Pt
import os
import subprocess

def convert_xlsx_to_docx(xlsx_path, docx_path, fileType, headers, headers_bold, font_size, font, form, original_name):
    font_size = (int(font_size))
    # file xlsx read
    df = pd.read_excel(xlsx_path)
    # dockx file creating
    doc = Document()
    header = original_name
    heading = doc.add_heading(header, level=1)
    for run in heading.runs:
        run.font.name = font
        run.font.size = Pt(font_size)

    columns_per_table = 10

    if form == 1:
        if df.shape[1] > 10:
            for start_col in range(0, df.shape[1], columns_per_table):
                end_col = min(start_col + columns_per_table, df.shape[1])
                sub_df = df.iloc[:, start_col:end_col]

                table = doc.add_table(rows=sub_df.shape[0] + 1, cols=sub_df.shape[1])
                table.style = 'Table Grid'
                if headers == True:
                    for j, column in enumerate(sub_df.columns):
                        cell = table.cell(0, j)
                        run = cell.paragraphs[0].add_run(str(column))
                        run.font.name = font
                        run.font.size = Pt(font_size)
                        if headers_bold:
                            run.bold = True

                for i, row in sub_df.iterrows():
                    for j, value in enumerate(row):
                        cell = table.cell(i + 1, j)
                        run = cell.paragraphs[0].add_run(str(value))
                        run.font.name = font
                        run.font.size = Pt(font_size)

                doc.add_paragraph("")
        else:
            # adding table to document
            table = doc.add_table(rows=df.shape[0] + 1, cols=df.shape[1])
            table.style = 'Table Grid'
            # adding headers
            if headers == True:
                for j, column in enumerate(df.columns):
                    cell = table.cell(0, j)
                    run = cell.paragraphs[0].add_run(str(column))
                    run.font.name = font
                    run.font.size = Pt(font_size)
                    if headers_bold:
                        run.bold = True
            # adding data from excel
            for i, row in df.iterrows():
                for j, value in enumerate(row):
                    cell = table.cell(i + 1, j)
                    run = cell.paragraphs[0].add_run(str(value))
                    run.font.name = font
                    run.font.size = Pt(font_size)
    elif form == 2:
        # adding data from excel
        header = ""
        if headers == True:
            for j, column in enumerate(df.columns):
                header += str(column) + " "
            p = doc.add_paragraph()
            run = p.add_run(header.strip())
            run.font.name = font
            run.font.size = Pt(font_size)
            if headers_bold:
                run.bold = True
        for i, row in df.iterrows():
            line_text = ""
            for value in row:
                line_text += str(value) + " "
            p = doc.add_paragraph()
            run = p.add_run(line_text.strip())
            run.font.name = font
            run.font.size = Pt(font_size)
    elif form == 3:
        for idx, row in df.iterrows():
            p_num = doc.add_paragraph()
            run_num = p_num.add_run(f"{idx + 1}.")
            run_num.font.name = font
            run_num.font.size = Pt(font_size)
            for col in df.columns:
                value = str(row[col])
                p = doc.add_paragraph()
                if headers == True:
                    run1 = p.add_run(f"{col}: ")
                    run1.font.name = font
                    run1.font.size = Pt(font_size)
                    if headers_bold:
                        run1.bold = True

                    run2 = p.add_run(value)
                    run2.font.name = font
                    run2.font.size = Pt(font_size)
                else:
                    run = p.add_run(f"{value}")
                run.font.name = font
                run.font.size = Pt(font_size)
            doc.add_paragraph("")
    else:
        for idx, row in df.iterrows():
            p_num = doc.add_paragraph()
            run_num = p_num.add_run(f"{idx + 1}.")
            run_num.font.name = font
            run_num.font.size = Pt(font_size)
            if headers_bold == True:
                run_num.font.bold = True
            for col in df.columns:
                value = str(row[col])
                p = doc.add_paragraph()
                if headers == True:
                    run1 = p.add_run(f"{col}: ")
                    run1.font.name = font
                    run1.font.size = Pt(font_size)
                    if headers_bold:
                        run1.bold = True

                    run2 = p.add_run(value)
                    run2.font.name = font
                    run2.font.size = Pt(font_size)
                else:
                    run = p.add_run(f"{value}")
                run.font.name = font
                run.font.size = Pt(font_size)
            if idx < len(df) - 1:
                doc.add_page_break()

    doc.save(docx_path)
    if fileType == True:
        filename = os.path.basename(docx_path)
        #Konwersja do pdf --- nalezy tu umiescic sciezke do libre w komputerze ale mozliwe ze masz ta sama
        subprocess.run(['/Applications/LibreOffice.app/Contents/MacOS/soffice', '--headless', '--convert-to', 'pdf', filename, '--outdir', 'tmp'], check=True)
        os.rename(f'tmp/{filename.replace(".docx",".pdf")}', filename.replace(".docx",".pdf"))
        os.remove(docx_path)



