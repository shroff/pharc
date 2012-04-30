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

from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

COMMASPACE = ", "

def send_mail(send_from, send_to, subject, text, files=[], server="localhost"):
    assert type(send_to) == list
    assert type(files) == list

    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject
    msg.preamble = text

    # for f in files:
    #     part = MIMEBase('application', "octet-stream")
    #     part.set_payload(open(file, "rb").read())
    #     Encoders.encode_base64(part)
    #     part.add_header('Content-Disposition', 'attachment; filename=%s"' % os.path.basename(f))
    #     mst.attach(part)
        
    smtp.smtplib.SMTP(server)
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.close()


if __name__ == "__main__":
    # send some email to test things
    pass
