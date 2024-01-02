#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  reports_interactions_matrix.py
#
#  Copyright 2023 cswaim <cswaim@jcrl.net>

from pathlib import Path
import os
from datetime import datetime
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.colors import blue
from reportlab.lib import colors
from reportlab.lib.units import cm, inch
from reportlab.pdfbase import pdfmetrics
from src import config as cfg
from src import reports_util as rptu

class CardsReports():
    """ print the cards to a txt file and pdf flie """
    # centered line
    c_template = "{:^35}"
    cw_template = "{:^35}\n"

    def __init__(self, autorun=False):
        """init print the cards report"""
        self.hd1 = cfg.event_title
        self.hd2 = cfg.event_subtitle
        self.hd_date = cfg.event_date
        if autorun:
            self.run()


    def print_card_header(self, hd1, hd2, date_line):
        """print the card headings"""

        # set date if not set
        if rptu.dt is None:
            rptu.set_rpt_date()

        # print form feed
        print("\f")    # ,end=''  prevents additional newline after ff
        # print report headers
        print(self.c_template.format(hd1))
        if hd2 is not None and hd2 != "":
            print(self.c_template.format(hd2))
        if date_line is not None and date_line != "":
            print(self.c_template.format(date_line))
        print("\n")

    def print_card_dtl(self, dtl_line):
        """print card detail line"""
        print(self.c_template.format(dtl_line))

    def card_print(self, card):
        """print card to console"""
        self.print_card_header(self.hd1, self.hd2, self.hd_date)
        print(self.c_template.format("--------------------"))
        print("{:>33}".format(f"id: {card.id}\n"))
        for s, label in enumerate(card.group_labels):
            print(f"    {cfg.session_labels[s]}:   {label}")

    def card_txt_header(self, ctxt, hd1, hd2, date_line):
        """write the card headers to txt file"""

        # set date if not set
        if rptu.dt is None:
            rptu.set_rpt_date()

        # write form feed
        ctxt.write("\f")
        # write report headers
        ctxt.write(self.cw_template.format(hd1))
        if hd2 is not None and hd2 != "":
            ctxt.write(self.cw_template.format(hd2))
        if date_line is not None and date_line != "":
            ctxt.write(self.cw_template.format(date_line))
        ctxt.write("\n")

    def card_txt(self, ctxt, card):
        """ write the cards to a txt file """
        self.card_txt_header(ctxt, self.hd1, self.hd2, self.hd_date)
        ctxt.write("{:>33}\n\n".format(f"id: {card.id}"))
        for s, label in enumerate(card.group_labels):
            #s += 1
            ctxt.write(f"    {cfg.session_labels[s]}:   {label}\n")

    def card_pdf_center_calc(self, txt, font, size):
        """calc the x axis value to center test"""
        text_width = pdfmetrics.stringWidth(txt, font, size)
        x_centered = ((3 * inch) - text_width ) / 2.0
        return x_centered

    def card_pdf_canvas(self):
        """set up pff canvas"""
        # create 3x5 card canvas
        cardpdf = Canvas(f'{cfg.datadir}cards.pdf', pagesize=(3 * inch, 5 * inch))
        cardpdf.setFont("Helvetica", 18)
        cardpdf.setFillColor(blue)
        return cardpdf

    def card_pdf(self, cardpdf, card):
        """ write the cards to a pdf
        https://realpython.com/creating-modifying-pdf/#creating-pdf-files-with-python-and-reportlab
        https://www.reportlab.com/docs/reportlab-userguide.pdf

        """
        # fonts for pdf
        hd1_fs = 18
        hd2_fs = 14
        hdd_fs = 12
        sess_lbl_fs = 10
        sess_text_fs = 14
        footer_fs = 8

        # print header
        cardpdf.setFont("Helvetica", hd1_fs)
        cardpdf.setFillColor(blue)
        x_centered = self.card_pdf_center_calc(self.hd1, "Helvetica", hd1_fs)
        init_y = 4.6
        cardpdf.drawString(x_centered, init_y * inch, self.hd1)
        # set start postion from bottom of form
        last_y = init_y
        if self.hd2 is not None and self.hd2 != "":
            last_y += -.3
            cardpdf.setFont("Helvetica-Oblique", hd2_fs)
            x_centered = self.card_pdf_center_calc(self.hd2, "Helvetica", hd2_fs)
            cardpdf.drawString(x_centered, last_y * inch, self.hd2)
        if self.hd_date is not None and self.hd_date != "":
            last_y += -.3
            cardpdf.setFont("Helvetica", hdd_fs)
            x_centered = self.card_pdf_center_calc(self.hd_date, "Helvetica", hdd_fs)
            cardpdf.drawString(x_centered, last_y * inch, self.hd_date)
        last_y += -.15
        cardpdf.line(.25 * inch, last_y * inch, 2.75 * inch, last_y * inch)

        # creating a multiline text using
        # textline and for loop
        last_y += -.3
        text = cardpdf.beginText(.5 * inch, last_y * inch)

        for n, label in enumerate(card.group_labels):
            #n += 1   # adj for 0 offset
            line = f"{cfg.session_labels[n]}:"
            text.setFont("Helvetica", sess_lbl_fs)
            text.setFillColor(colors.black)
            text.textOut(line)
            line = f"   {label}"
            text.setFont("Helvetica", sess_text_fs)
            text.setFillColor(colors.red)
            text.textOut(line)
            text.textLine(text='')          #new line
        cardpdf.drawText(text)
        # end page
        cardpdf.setFont("Helvetica", footer_fs)
        cardpdf.setFillColor(colors.black)
        id_line = f'id: {card.id}'
        cardpdf.drawString(2.5 * inch, .2 * inch, id_line)
        cardpdf.showPage()

    def run(self,):
        #open pdf file object
        cpdf = self.card_pdf_canvas()
        with open(f'{cfg.datadir}cards.txt', 'w') as ctxt:
            for c in cfg.all_cards:
                # self.card_print(c)
                self.card_pdf(cpdf, c)
                self.card_txt(ctxt, c)
        # close the pdf file
        cpdf.save()

if __name__ == '__main__':
    # set the config file working directory
    wkdir = str(Path(__file__).resolve().parent) + os.pathsep
    cr = CardsReports()
    cr.run()