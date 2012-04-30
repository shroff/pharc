#!/usr/bin/env python

# PHARC: a photo archiving application for physicians
# Copyright (C) 2012 Saul Reynolds-Haertle
# 
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

import os,sys,getopt,struct, subprocess
from cStringIO import StringIO
from odf.opendocument import OpenDocumentPresentation
from odf.style import Style, MasterPage, PageLayout, PageLayoutProperties, \
TextProperties, GraphicProperties, ParagraphProperties, DrawingPageProperties
from odf.text import P
from odf.draw  import Page, Frame, TextBox, Image

import PIL.Image


def export_presentation(photos, destination, openafter=False):
    if destination[-4:] != ".odp": destination += ".odp"
    
    doc = OpenDocumentPresentation()

    # We must describe the dimensions of the page
    pagelayout = PageLayout(name="Layout")
    doc.automaticstyles.addElement(pagelayout)
    pagelayout.addElement(PageLayoutProperties(margin="0pt", pagewidth="800pt", pageheight="600pt", printorientation="landscape"))

    # Style for the title frame of the page
    # We set a centered 34pt font with yellowish background
    titlestyle = Style(name="Master-title", family="presentation")
    titlestyle.addElement(ParagraphProperties(textalign="center"))
    titlestyle.addElement(TextProperties(fontsize="34pt"))
    titlestyle.addElement(GraphicProperties(fillcolor="#ffffff"))
    doc.styles.addElement(titlestyle)

    # Style for the photo frame
    photostyle = Style(name="Master-photo", family="presentation")
    doc.styles.addElement(photostyle)

    # Create automatic transition
    dpstyle = Style(name="dp1", family="drawing-page")
    # dpstyle.addElement(DrawingPageProperties(transitiontype="automatic", transitionstyle="move-from-top", duration="PT5S"))
    doc.automaticstyles.addElement(dpstyle)

    # Every drawing page must have a master page assigned to it.
    masterpage = MasterPage(name="Master", pagelayoutname=pagelayout)
    doc.masterstyles.addElement(masterpage)
    
    for p in photos:
        path = p.getData()
        i = PIL.Image.open(path)
        (w, h) = i.size
        if w > 720:
           h = float(h) * 720.0 / float(w)
           w = 720.0
        if h > 540.0:
           w = float(w) * 540.0 / float(h)
           h = 540.0

        page = Page(stylename=dpstyle, masterpagename=masterpage)
        doc.presentation.addElement(page)
        titleframe = Frame(stylename=titlestyle, width="720pt",
           height="56pt", x="40pt", y="10pt")
        page.addElement(titleframe)
        textbox = TextBox()
        titleframe.addElement(textbox)
        textbox.addElement(P(text=p.name))

        offsetx = 400.0 - w/2.0
        photoframe = Frame(stylename=photostyle, width="%fpt" % w,
           height="%fpt" % h, x="%fpt" % offsetx, y="56pt")
        page.addElement(photoframe)
        href = doc.addPicture(path)
        photoframe.addElement(Image(href=href))
    
    doc.save(destination)


    if sys.platform.startswith('darwin'):
        subprocess.call(('open', destination))
    elif os.name == 'nt':
        os.startfile(detination)
    elif os.name == 'posix':
        subprocess.call(('xdg-open', destination))
