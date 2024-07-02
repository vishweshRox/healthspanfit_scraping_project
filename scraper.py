#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 19:34:02 2024

@author: vishweshpalani
"""

import imaplib
import email
import csv
import re


import yaml  #To load saved login credentials from a yaml file

with open("c1.yml") as f:
    content = f.read()
    
# from credentials.yml import user name and password
my_credentials = yaml.load(content, Loader=yaml.FullLoader)

#Load the user name and passwd from yaml file
user, password = my_credentials["user"], my_credentials["password"]

#easier process

user = "<EMAIL ADDRESS>"
password = "<APP PASSWORD>"

#URL for IMAP connection
#imap_url = 'imap.gmail.com'
imap_url = 'imap.mail.yahoo.com'

mb = imaplib.IMAP4_SSL(imap_url)
rv, message = mb.login(user, password)
# 'OK', [b'LOGIN completed']

# 'OK', [b'22']



# Download a message

emails = []
email_pattern = r'<([^>]+)>'

a = 15


def extract_emails(text):
    # Regular expression pattern to match email addresses
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    # Find all matches using findall()
    emails = re.findall(pattern, text)

    return emails

mailbox_list = ["Inbox"]

for mailbox in mailbox_list:
    
    try:
        rv, num_emails = mb.select(mailbox)
    except:
        continue
    
    print("starting:", mailbox)
    
    if mailbox == "Sent": counter = 2154
    else: counter = 1
    s_r = bytes(str(counter), 'utf-8')
    typ, data = mb.fetch(s_r, '(RFC822)')
    if data != None:
        if data[0] != None:
            msg = email.message_from_bytes(data[0][1])
        else: msg = None
    else: msg = None
    
    # Parse the email
    msg = email.message_from_bytes(data[0][1])
    
    while(msg != None):
        
        add = lambda s: msg[s] != None
        
        if add('From'): emails.extend(extract_emails(msg['From'])) 
        if add('To'): emails.extend(extract_emails(msg['To']))  
        if add('Cc'): emails.extend(extract_emails(msg['Cc']))  
        if add('Bcc'): emails.extend(extract_emails(msg['Bcc']))  
        counter += 1
        
        if counter % 100 == 0:
            emails = list(set(emails))
            print('____________')
            print("count:", counter)
            print('____________')
            print(emails)
            print('LENGTH: ', len(emails))
            csv_file_path = 'new_data.csv'
            # Write data to the CSV file
            with open(csv_file_path, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                for e in emails:
                    writer.writerow([e])
            print("Data has been written to", csv_file_path)
            
        #next
        try:
            s_r = bytes(str(counter), 'utf-8')
            typ, data = mb.fetch(s_r, '(RFC822)')
            if data != None:
                if data[0] != None:
                    msg = email.message_from_bytes(data[0][1])
                else: msg = None
            else: msg = None
        except: 
            print("Error:", s_r)
            break
    
    emails = list(set(emails))
    print('____________')
    print("mailbox:", mailbox)
    print('____________')
    print(emails)
    print('LENGTH: ', len(emails))
    csv_file_path = 'new_data.csv'
    # Write data to the CSV file
    with open(csv_file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for e in emails:
            writer.writerow([e])
    print("Data has been written to", csv_file_path)

    
    
        
print('____________')
print('FINAL')
print('____________')
emails = list(set(emails))

print(emails)


csv_file_path = 'new_data.csv'

# Write data to the CSV file
with open(csv_file_path, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    for e in emails:
        writer.writerow([e])


print("Data has been written to", csv_file_path)
