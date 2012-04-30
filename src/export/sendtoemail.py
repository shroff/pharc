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

import smtplib
import os
import sys
import multiprocessing

import dns.resolver as dnsr

from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
import email.encoders

from PyQt4.QtCore import *

class ExportThread(QThread):
    def __init__(self, parent=None):
        super(ExportThread, self).__init__(parent)

    def __del__(self):
        self.wait()

    def export(self, photos, destination):
        self.photos = photos
        self.destination = destination
        self.start()

    def run(self):
        result = None
        print("sending email")

        msg = MIMEMultipart()
        msg['From'] = self.destination
        msg['To'] = self.destination
        msg['Subject'] = "PHARC export"

        i = 0
        for p in self.photos:
            part = MIMEBase('application', "octet-stream")
            part.set_payload(open(p.getData(),"rb").read())
            email.encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment; filename="image %d: %s - %s"' % (i, p.photoset.patient.name(), p.name))
            i = i+1
            msg.attach(part)

        (user, server) = self.destination.split("@")
        
        try:
            host = ""
            ans = dnsr.query(server, "MX")
            for d in ans:
                host = str(d.exchange)
        except Exception:
            result = -1

        if result is None:
            try:
                s = smtplib.SMTP(host + ":25", timeout=5)
                s.sendmail(self.destination, [self.destination], msg.as_string())
                print("sent email")
                result = 0
            except Exception:
                print("An exception!")
                result = -2
            finally:
                s.quit()

        print("done with email")
        self.emit(SIGNAL("emailExportDone(int)"),
                  result)
                  
