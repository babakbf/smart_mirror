# -*- coding: utf-8 -*-
"""
Created on Mon Jan 11 21:22:44 2021

@author: babak
"""

import smtplib

from email.message import EmailMessage

body = "MINIIIIIIIIIIIIIIIIIIIS"
msg = EmailMessage()
msg.set_content(body)
msg['subject'] = 'MINIS'
msg['to']= 'babakbf@gmail.com'
user = 'bob.iot.smart@gmail.com'
password = '**************'
msg['from'] = user
server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()
server.login(user, password)
server.send_message(msg)

server.quit()