# https://stackabuse.com/creating-pdf-invoices-in-python-with-borb/

from borb.pdf import Document, Page, SingleColumnLayoutWithOverflow, Paragraph
from borb.pdf.canvas.layout.table.table import Table, TableCell

from borb.pdf.pdf import PDF
from borb.pdf.canvas.color.color import HexColor, X11Color
from borb.pdf import FixedColumnWidthTable

from decimal import Decimal
from datetime import datetime

import pandas as pd
import os


# Define a function for recursive directory removal
def remove_directory(path):
    if os.path.exists(path):
        for root, dirs, files in os.walk(path, topdown=False):
            for name in files:
                file_path = os.path.join(root, name)
                os.remove(file_path)
            for name in dirs:
                dir_path = os.path.join(root, name)
                os.rmdir(dir_path)
        os.rmdir(path)
    return


max_notitie_tekst = 200

# verwijder map met oude bestanden
remove_directory("./output_pdf")

encoding_default = "utf-8"
encoding_windows = "cp1252"

df = pd.read_csv("./input/retrieve_all_notities_uitzonderingen_x.csv", sep=';', quotechar='"', dtype=str, encoding=encoding_default)
df.fillna("", inplace=True)  # vervang NaN door ""
df["SQUITXO_ZAAKNUMMER"] = df["SQUITXO_ZAAKNUMMER"].str.lstrip()  # verwijder voorloop spatie

unieke_zaak_ids = list(df['HOOFDZAAKID'].unique())

for zaak_id in unieke_zaak_ids:
    print("working on: " + zaak_id)
    zaak_df = df.loc[df['HOOFDZAAKID'] == zaak_id]

    sxo_zaak_txt = str(zaak_df.iloc[0]["SQUITXO_ZAAKNUMMER"]).rstrip()
    if len(sxo_zaak_txt) == 0:
        sxo_zaak_txt = "SquitXo zaaknummer niet ingevuld"
    print("working on: " + sxo_zaak_txt)

    ext_zaak_txt = str(zaak_df.iloc[0]["EXTERN_ZAAKNUMMER"]).rstrip()
    if len(ext_zaak_txt) == 0:
        ext_zaak_txt = "Extern zaaknummer niet ingevuld"

    glob_loc_txt = str(zaak_df.iloc[0]["GLOBALE_LOCATIE"]).rstrip()
    if len(glob_loc_txt) == 0:
        glob_loc_txt = "Globale locatie niet ingevuld"

    oms_zaak_txt = str(zaak_df.iloc[0]["OMSCHRIJVING"].rstrip())
    if len(oms_zaak_txt) == 0:
        oms_zaak_txt = "Omschrijving niet gevuld"

    folder_id = sxo_zaak_txt.replace(" ", "_")
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
        FixedColumnWidthTable(number_of_columns=2, number_of_rows=10)
            # row1
            # set column_span to 2
            .add(TableCell(
                    Paragraph("Export gegevens uit SquitXO op " + now.strftime("%Y-%m-%d %H:%M:%S") + "\n",
                              font_size=Decimal(8)),
                    column_span=2))

            # row2 lege regel
            .add(TableCell(
                    Paragraph(" ", font="Helvetica-Bold"),
                    column_span=2))

            # row3
            .add(Paragraph("SquitXO zaaknummer:",
                           font="Helvetica-Bold"))
            .add(Paragraph(sxo_zaak_txt,
                           font="Courier"))
            # row4
            .add(Paragraph("Extern zaaknummer:",
                           font="Helvetica-Bold"))
            .add(Paragraph(ext_zaak_txt,
                           font="Courier"))

            # row5 lege regel
            .add(TableCell(Paragraph(" ", font="Helvetica-Bold"),
                           column_span=2))

            # row6
            .add(TableCell(Paragraph("Locatie:", font="Helvetica-Bold"),
                           column_span=2))
            # row7
            .add(TableCell(Paragraph(glob_loc_txt,
                                     font="Courier"),
                           column_span=2))

           # row8 lege regel
            .add(TableCell(Paragraph(" ", font="Helvetica-Bold"),
                           column_span=2))

            # row9
            .add(TableCell(Paragraph("Zaak omschrijving",
                                     font="Helvetica-Bold"),
                           column_span=2))
            # row10
            .add(TableCell(Paragraph(oms_zaak_txt,
                                     font="Courier"),
                           column_span=2))

            .set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
            .no_borders()
    )

    page_layout.add(Paragraph(""))

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
        notitie_tekst = notitie_tekst.replace("￻  \n", "")
        notitie_tekst = notitie_tekst.replace("C", '"')
        notitie_tekst = notitie_tekst.replace("≤", '<=')

        if zaak_id in ["27420344", "16091262", "3907881", "33473003", "9247714", "5307071", "2265120"]:
            print("=======================================================================")
            print("SquitXO nummer     :", sxo_zaak_txt)
            print("Lengte notitietekst:", str(len(notitie_tekst)))
            print(str(row["NOTITIE_OPSTELLER"].rstrip()))
            print(str(row["NOTITIE_DATUM"].rstrip()))
            print(notitie_tekst)

        if len(notitie_tekst) == 0:
            notitie_tekst = "Notitieveld niet ingevuld"

        # create a FixedColumnWidthTable
        page_layout.add(
            FixedColumnWidthTable(number_of_columns=6,
                                  number_of_rows=1,
                                  background_color=alternating_colors[row_index % 2])
                # row1 col1
                .add(TableCell(
                        Paragraph("Datum",
                                  font="Helvetica-Bold",
                                  background_color=alternating_colors[row_index % 2]),
                        border_left=False,
                        border_top=False,
                        border_right=False))
                # row1 col2+3
                .add(TableCell(
                        Paragraph(f'{row["NOTITIE_DATUM"]}',
                                  font="Courier",
                                  background_color=alternating_colors[row_index % 2]),
                        column_span=2,
                        border_left=False,
                        border_top=False,
                        border_right=False))
                # row1 col 4
                .add(TableCell(
                        Paragraph("Opsteller",
                                  font="Helvetica-Bold",
                                  background_color=alternating_colors[row_index % 2]),
                        border_left=False,
                        border_top=False,
                        border_right=False))
                # row 1 col5+6
                .add(TableCell(
                        Paragraph(f'{row["NOTITIE_OPSTELLER"]}',
                                  font="Courier",
                                  background_color=alternating_colors[row_index % 2]),
                        column_span=2,
                        border_left=False,
                        border_top=False,
                        border_right=False))
                .set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
                # .no_borders()
        )
        if len(notitie_tekst) < max_notitie_tekst:
            page_layout.add(
                FixedColumnWidthTable(number_of_columns=1,
                                      number_of_rows=1,
                                      background_color=alternating_colors[row_index % 2])
                # row1 col1
                .add(TableCell(
                        Paragraph(f'{notitie_tekst}',
                                  font="Courier",
                                  background_color=alternating_colors[row_index % 2]),
                        border_left=False,
                        border_top=False,
                        border_right=False,
                        border_bottom=False))
            )
        else:
            n = len(notitie_tekst)/max_notitie_tekst
            aantal_blokken = int(n) + ((int(n) - n) != 0)  # round up n
            i = 0
            while i < aantal_blokken:
                print(i)
                start_punt = i * max_notitie_tekst
                print(start_punt)
                eind_punt = (i+1) * max_notitie_tekst
                print(eind_punt)
                not_part = notitie_tekst[start_punt:eind_punt]  # deel van de tekst
                page_layout.add(
                    FixedColumnWidthTable(number_of_columns=1,
                                          number_of_rows=1,
                                          border_width=Decimal(0),
                                          border_left=False,
                                          border_top=False,
                                          border_right=False,
                                          border_bottom=False,
                                          background_color=alternating_colors[row_index % 2])
                        # row1 col1
                        .add(TableCell(
                                Paragraph(f'{not_part}',
                                          font="Courier",
                                          border_width=Decimal(0),
                                          border_left=False,
                                          border_top=False,
                                          border_right=False,
                                          border_bottom=False,
                                          background_color=alternating_colors[row_index % 2]),
                                border_width=Decimal(0),
                                border_left=False,
                                border_top=False,
                                border_right=False,
                                border_bottom=False))
                )
                
                i += 1

        page_layout.add(Paragraph(""))

        row_index += 1

    output_dir = "./output_pdf/" + folder_id + "/"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(output_dir + "notities.pdf", "wb") as pdf_file_handle:
        PDF.dumps(pdf_file_handle, pdf)
