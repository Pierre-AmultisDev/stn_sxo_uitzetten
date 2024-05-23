# https://stackabuse.com/creating-pdf-invoices-in-python-with-borb/

from borb.pdf import Document, Page, SingleColumnLayout, SingleColumnLayoutWithOverflow, Paragraph
from borb.pdf.canvas.layout.table.table import Table, TableCell
# from borb.pdf.canvas.layout.page_layout.multi_column_layout import MultiColumnLayout
# from borb.pdf.canvas.layout.page_layout.single_column_layout import SingleColumnLayout
from borb.pdf.pdf import PDF
from borb.pdf.canvas.color.color import HexColor, X11Color
from borb.pdf import FlexibleColumnWidthTable
from borb.pdf import FixedColumnWidthTable

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


df = pd.read_csv("./input/retrieve_all_notities.csv", sep=';', quotechar='"', dtype=str)
df.fillna("", inplace=True)

unieke_zaak_ids = list(df['HOOFDZAAKID'].unique())

for zaak_id in unieke_zaak_ids:
    print("working on: " + zaak_id)
    zaak_df = df.loc[df['HOOFDZAAKID'] == zaak_id]

    sxo_zaak_txt = str(zaak_df.iloc[0]["SQUITXO_ZAAKNUMMER"]).rstrip()
    if len(sxo_zaak_txt) == 0:
        ext_zaak_txt = "Niet gevuld"

    ext_zaak_txt = str(zaak_df.iloc[0]["EXTERN_ZAAKNUMMER"]).rstrip()
    if len(ext_zaak_txt) == 0:
        ext_zaak_txt = "Niet gevuld"

    glob_loc_txt = str(zaak_df.iloc[0]["GLOBALE_LOCATIE"]).rstrip()
    if len(glob_loc_txt) == 0:
        ext_zaak_txt = "Niet gevuld"

    oms_zaak_txt = str(zaak_df.iloc[0]["OMSCHRIJVING"].rstrip())
    if len(glob_loc_txt) == 0:
        oms_zaak_txt = "Niet gevuld"

    # Create document per zaak_id
    pdf = Document()

    # Add page
    page = Page()
    pdf.add_page(page)

    # Create Layout
    # page_layout = SingleColumnLayout(page)
    page_layout = SingleColumnLayoutWithOverflow(page)

    page_layout.vertical_margin = page.get_page_info().get_height() * Decimal(0.02)

    now = datetime.now()

    # create a FixedColumnWidthTable
    page_layout.add(
        FixedColumnWidthTable(number_of_columns=2, number_of_rows=7)
            # row1
            # set column_span to 2
            .add(TableCell(
                    Paragraph("Export gegevens uit SquitXO op " + now.strftime("%Y-%m-%d %H:%M:%S") + "\n"),
                    col_span=2))
            # row2
            .add(Paragraph("SquitXO zaaknummer:",
                           font="Helvetica-Bold"))
            .add(Paragraph(sxo_zaak_txt,
                           font="Courier"))
            # row3
            .add(Paragraph("Extern zaaknummer:",
                           font="Helvetica-Bold"))
            .add(Paragraph(ext_zaak_txt,
                           font="Courier"))
            # row4
            .add(TableCell(Paragraph("Locatie:",
                                     font="Helvetica-Bold"),
                           col_span=2))
            # row5
            .add(TableCell(Paragraph(glob_loc_txt,
                                     font="Courier"),
                           col_span=2))
            # row6
            .add(TableCell(Paragraph("Zaak omschrijving",
                                     font="Helvetica-Bold"),
                           col_span=2))
            # row7
            .add(TableCell(Paragraph(oms_zaak_txt,
                                     font="Courier"),
                           col_span=2))

            .set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
            .no_borders()
    )

    page_layout.add(Paragraph(""))

    # # Paragraph with export timestamp
    # page_layout.add(Paragraph("Export gegevens uit SquitXO op " + now.strftime("%Y-%m-%d %H:%M:%S")))
    #
    # page_layout.add(Paragraph("SquitXO zaaknummer:", font="Helvetica-Bold"))
    # page_layout.add(Paragraph(sxo_zaak_txt, font="Courier"))
    #
    # page_layout.add(Paragraph("Extern  zaaknummer:", font="Helvetica-Bold"))
    # page_layout.add(Paragraph(ext_zaak_txt, font="Courier"))
    #
    # page_layout.add(Paragraph("Locatie:", font="Helvetica-Bold"))
    # page_layout.add(Paragraph(glob_loc_txt, font="Courier"))
    #
    # page_layout.add(Paragraph("Zaak omschrijving", font="Helvetica-Bold"))
    # page_layout.add(Paragraph(oms_zaak_txt, font="Courier"))

    # Voeg de inhoud van het DataFrame toe aan de PDF met afwisselende achtergrondkleuren
    alternating_colors = [HexColor("FFFFFF"), HexColor("F0F0F0")]  # wit en lichtgrijs

    notitie_df = zaak_df[["NOTITIE_ONDERWERP", "NOTITIE_OPSTELLER", "NOTITIE_DATUM", "NOTITIE_TEKST_CLEAN"]].copy()
    notitie_df.sort_values(by=["NOTITIE_DATUM"], ascending=False, inplace=True)

    print('aantal rijen   :', str(len(notitie_df)))

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

        # create a FixedColumnWidthTable
        page_layout.add(
            FixedColumnWidthTable(number_of_columns=4,
                                  number_of_rows=2,
                                  background_color=alternating_colors[row_index % 2])
                .add(Paragraph("Datum",
                               font="Helvetica-Bold",
                               background_color=alternating_colors[row_index % 2]))
                .add(Paragraph(f'{row["NOTITIE_DATUM"]}',
                               font="Courier",
                               background_color=alternating_colors[row_index % 2]))
                .add(Paragraph("Opsteller",
                               font="Helvetica-Bold",
                               background_color=alternating_colors[row_index % 2]))
                .add(Paragraph(f'{row["NOTITIE_OPSTELLER"]}',
                               font="Courier",
                               background_color=alternating_colors[row_index % 2]))

                # set column_span to 4
                .add(TableCell(Paragraph(notitie_tekst,
                                         font="Courier",
                                         background_color=alternating_colors[row_index % 2]),
                               col_span=4))
                .set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
                .no_borders()
        )
        page_layout.add(Paragraph(""))

        row_index += 1

    output_dir = "./output_pdf/" + zaak_id + "/"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(output_dir + "notities.pdf", "wb") as pdf_file_handle:
        PDF.dumps(pdf_file_handle, pdf)

