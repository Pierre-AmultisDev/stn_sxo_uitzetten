# https://stackabuse.com/creating-pdf-invoices-in-python-with-borb/

from borb.pdf import Document, Page, SingleColumnLayout, SingleColumnLayoutWithOverflow, Paragraph
from borb.pdf.canvas.layout.table.table import Table, TableCell
# from borb.pdf.canvas.layout.page_layout.multi_column_layout import MultiColumnLayout
# from borb.pdf.canvas.layout.page_layout.single_column_layout import SingleColumnLayout
from borb.pdf.pdf import PDF
from borb.pdf.canvas.color.color import HexColor, X11Color

# from borb.pdf.document.document import Document
# from borb.pdf.page.page import Page
# from borb.pdf.pdf import PDF
# from borb.pdf import HexColor
#
# from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
# from borb.pdf.canvas.layout.table.fixed_column_width_table import FixedColumnWidthTable as Table
# from borb.pdf.canvas.layout.text.paragraph import Paragraph
# from borb.pdf.canvas.layout.layout_element import Alignment

from decimal import Decimal
from datetime import datetime
import random

import pandas as pd
import os


def build_document_header_information(hoofdzaak, externnr, locatie, omschrijving):
    table = Table(number_of_rows=4, number_of_columns=2)

    # row1
    table.add(Paragraph("SquitXO zaaknummer:", font="Helvetica-Bold"))
    table.add(Paragraph(hoofdzaak, font="Courier"))

    # row2
    table.add(Paragraph("Extern  zaaknummer:", font="Helvetica-Bold"))
    table.add(Paragraph(externnr, font="Courier"))

    # row3
    table.add(Paragraph("Locatie:", font="Helvetica-Bold"))
    table.add(Paragraph(locatie, font="Courier"))

    # row4
    table.add(Paragraph("Zaak omschrijving", font="Helvetica-Bold"))
    table.add(Paragraph(omschrijving, font="Courier"))

    table.set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
    table.no_borders()
    return table


def build_document_notes_info_block(not_opsteller, not_datum):
    table = Table(number_of_rows=2, number_of_columns=2)

    # row1
    #table.add(Paragraph("Notitie onderwerp", font="Helvetica-Bold"))
    #table.add(Paragraph(not_onderwerp, font="Courier"))

    # row2
    table.add(Paragraph("Notitie opsteller", font="Helvetica-Bold"))
    table.add(Paragraph("Notitie datum", font="Helvetica-Bold"))

    # row3
    table.add(Paragraph(not_opsteller, font="Courier"))
    table.add(Paragraph(not_datum, font="Courier"))

    table.no_borders()
    return table


def build_document_notes_block(note):
    table = Table(number_of_rows=1, number_of_columns=1)

    # row1
    table.add(Paragraph(note, font="Courier"))

    table.no_borders()
    return table


df = pd.read_csv("./input/retrieve_all_notities.csv", sep=';', quotechar='"', dtype=str)
df.fillna("", inplace=True)

unieke_zaak_ids = list(df['HOOFDZAAKID'].unique())

for zaak_id in unieke_zaak_ids:
    print("working on: " + zaak_id)
    zaak_df = df.loc[df['HOOFDZAAKID'] == zaak_id]

    sxo_zaak_txt = str(zaak_df.iloc[0]["SQUITXO_ZAAKNUMMER"]).rstrip()
    ext_zaak_txt = str(zaak_df.iloc[0]["EXTERN_ZAAKNUMMER"]).rstrip()
    glob_loc_txt = str(zaak_df.iloc[0]["GLOBALE_LOCATIE"]).rstrip()
    oms_zaak_txt = str(zaak_df.iloc[0]["OMSCHRIJVING"].rstrip())

    # Create document per zaak_id
    pdf = Document()

    # Add page
    page = Page()
    pdf.add_page(page)

    # Create Layout
    # page_layout = SingleColumnLayout(page)
    page_layout = SingleColumnLayoutWithOverflow(page)

    page_layout.vertical_margin = page.get_page_info().get_height() * Decimal(0.02)

    # Paragraph with export timestamp
    now = datetime.now()
    page_layout.add(Paragraph("Export gegevens uit SquitXO op " + now.strftime("%Y-%m-%d %H:%M:%S")))

    page_layout.add(Paragraph("SquitXO zaaknummer:", font="Helvetica-Bold"))
    page_layout.add(Paragraph(sxo_zaak_txt, font="Courier"))

    page_layout.add(Paragraph("Extern  zaaknummer:", font="Helvetica-Bold"))
    page_layout.add(Paragraph(ext_zaak_txt, font="Courier"))

    page_layout.add(Paragraph("Locatie:", font="Helvetica-Bold"))
    page_layout.add(Paragraph(glob_loc_txt, font="Courier"))

    page_layout.add(Paragraph("Zaak omschrijving", font="Helvetica-Bold"))
    page_layout.add(Paragraph(oms_zaak_txt, font="Courier"))

    # Voeg de inhoud van het DataFrame toe aan de PDF met afwisselende achtergrondkleuren
    alternating_colors = [HexColor("FFFFFF"), HexColor("F0F0F0")]  # wit en lichtgrijs

    notitie_df = zaak_df[["NOTITIE_ONDERWERP", "NOTITIE_OPSTELLER", "NOTITIE_DATUM", "NOTITIE_TEKST_CLEAN"]]
    print('aantal rijen   :', str(len(notitie_df)))
    print('aantal kolommen:', str(len(notitie_df.columns)))
    table = Table(number_of_rows=len(notitie_df)*len(notitie_df.columns), number_of_columns=1)

    row_index = 0
    for index, row in notitie_df.iterrows():
        print(row_index)

        notitie_tekst = str(row["NOTITIE_TEKST_CLEAN"].rstrip())
        notitie_tekst = notitie_tekst.replace("", "")
        notitie_tekst = notitie_tekst.replace("C", '"')
        notitie_tekst = notitie_tekst.replace("≤", '<=')

        if zaak_id in ["27420344", "16091262", "3907881", "33473003", "9247714", "5307071", "2265120"]:
            print(notitie_tekst)
            print(str(row["NOTITIE_OPSTELLER"].rstrip()))
            print(str(row["NOTITIE_DATUM"].rstrip()))

        for col in notitie_df.columns:
            # Toon de column name op 1 regel
            cell_text = f'{col}'
            print(cell_text)

            table.add(
                TableCell(
                    Paragraph(cell_text, background_color=alternating_colors[row_index % 2]),
                    background_color=alternating_colors[row_index % 2]
                )
            )

            # toon de column text op de volgende regel
            if col == "NOTITIE_TEKST_CLEAN":
                cell_text = f'{notitie_tekst}'
            else:
                cell_text = f'{row[col]}'

            print(cell_text)
            table.add(
                TableCell(
                    Paragraph(cell_text, background_color=alternating_colors[row_index % 2]),
                    background_color=alternating_colors[row_index % 2]
                )
            )

        row_index += 1

    page_layout.add(table)

    output_dir = "./output_pdf/" + zaak_id + "/"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(output_dir + "notities.pdf", "wb") as pdf_file_handle:
        PDF.dumps(pdf_file_handle, pdf)

