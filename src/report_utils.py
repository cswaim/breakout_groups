#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  report_utilities.py
#
#  Copyright 2023 cswaim <cswaim@jcrl.net>

"""
    Common routines used by the reporting modules

    from src import report_utils as rptu
"""

from datetime import datetime
from src import config as cfg

dt = None
hd1_template = """ Date: {} {:^50} Time: {}"""
hd2_template = """             {:^50} """

col1_template = """ {}"""
col2_template = """ {}"""

def set_rpt_date(rpt_date=None):
    """set the report date"""
    global dt
    if rpt_date is None:
        dt = datetime.now()
    else:
        dt = rpt_date

def print_header(hd1, hd2=None, col_hd1=None, col_hd2=None,fmt="std"):
    """print report header"""
    # set date if not set
    if dt is None:
        set_rpt_date()

    print("")
    # print report headers
    if fmt == "std":
        print(hd1_template.format(dt.strftime("%y-%m-%d"), hd1, dt.strftime("%H:%M:%S")))
    else:
        print(f"{hd1}")
    if hd2 is not None:
        if fmt == "std":
            print(hd2_template.format(hd2))
        else:
            print(f"{hd2}")

    # print column headings
    if col_hd1 is not None:
        print(col1_template.format(col_hd1))
    if col_hd2 is not None:
        print(col2_template.format(col_hd2))

def print_dtl(line):
    """print detail report line"""
    print(line)

def print_card_header(hd1, hd2,):
    """print the card headings"""
    ch1 = "{:^35}"

    # set date if not set
    if dt is None:
        set_rpt_date()

    print("")
    # print report headers
    print(ch1.format(hd1))
    if hd2 is not None:
        print(ch1.format(hd2))

    print("\n")

def card_pdf():
    """https://realpython.com/creating-modifying-pdf/#creating-pdf-files-with-python-and-reportlab
    https://www.reportlab.com/docs/reportlab-userguide.pdf

    """
    textlines = ['red', 'Portales', 'Massive', 'group1', 'green', 'Santa Fe', ]

    from reportlab.pdfgen.canvas import Canvas
    from reportlab.lib.colors import blue
    from reportlab.lib import colors
    from reportlab.lib.units import cm, inch
    from reportlab.pdfbase import pdfmetrics
    # create 3x5 card canvas
    cardpdf = Canvas(f'{cfg.datadir}cards.pdf', pagesize=(3 * inch, 5 * inch))
    cardpdf.setFont("Helvetica", 24)
    cardpdf.setFillColor(blue)
    title = "My Title"
    text_width = pdfmetrics.stringWidth(title, "Helvetica", 24)
    x_centered = ((3 * inch) - text_width ) / 2.0
    cardpdf.drawString(x_centered, 4.7 * inch, title)
    cardpdf.line(.5 * inch, 4.5 * inch, 2.5 * inch, 4.5 * inch)

    # creating a multiline text using
    # textline and for loop
    cardpdf.setFont("Helvetica", 18)
    text = cardpdf.beginText(.5 * inch, 4 * inch)
    text.setFont("Courier", 18)
    text.setFillColor(colors.red)
    for line in textlines:
        text.textLine(line)
    cardpdf.drawText(text)
    # end page
    cardpdf.showPage()
    cardpdf.save()