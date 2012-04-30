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

if sys.version_info[0] == 2:
    import dns.resolver as dnsr
if sys.version_info[0] == 3:
    import dns.resolver as dnsr

from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
import email.encoders

def export_email(photos, destination):
    msg = MIMEMultipart()
    msg['From'] = destination
    msg['To'] = destination
    msg['Subject'] = "PHARC export"

    i = 0
    for p in photos:
        part = MIMEBase('application', "octet-stream")
        part.set_payload(open(p.getData(),"rb").read())
        email.encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="image %d: %s - %s"' % (i, p.photoset.patient.name(), p.name))
        i = i+1
        msg.attach(part)

    (user, server) = destination.split("@")
    
    host = ""
    ans = dnsr.query(server, "MX")
    for d in ans:
        host = str(d.exchange)
    s = smtplib.SMTP(host + ":25")
    s.sendmail(destination, [destination], msg.as_string())
    s.quit()
