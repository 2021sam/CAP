import os
import sys
import json
import time
import ftplib
import requests
import smtplib
from pathlib import Path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from ftplib import FTP, error_perm
from credentials import server_ip, server_email_address, server_email_password, recipients, ftp_host, ftp_user, ftp_password
# find . -name 'ip.txt'


def get_last_known_ip(path_file_name):
    if not path_file_name.is_file():
        print('Does not exist !')
        return

    if path_file_name.is_file():
        f = open(path_file_name, 'r')
        ip = f.read()
        f.close()
        print(f'Last ip: {ip}')
        return ip

def get_wan_ip():
    ip = requests.get('https://api.ipify.org').content.decode('utf8')
    print(f'Live ip: {ip}')
    return ip

def update_ip(file_name, wan_ip):
    f = open(file_name, 'w')
    f.write(wan_ip)
    f.close()
    print(f'Saved new ip: {wan_ip}')

def upload_file(ftp, remote, path_file_name, file_name):
    ftp.cwd( remote )
    ftp.storbinary('STOR ' + file_name, open(path_file_name, 'rb'))
    print(f'Uploaded: {file_name}')


def ftp(remote, path_file_name, file_name):
    ftp = None
    try:
        print(ftp_host)
        ftp = FTP(ftp_host)
        login_code = ftp.login(user=ftp_user, passwd=ftp_password)
        # login_code = login_code.split()
        print(login_code)
        # login_code = login_code[0]
        upload_file(ftp, remote, path_file_name, file_name)
        ftp.quit()

    except Exception as e:
        print('Exception ', e)

    finally:
        print( '.', end='' )


def notify(subject, body):
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    print('notify')
    msg = MIMEMultipart()
    msg['From'] = server_email_address
    msg['To'] =  ", ".join( recipients )
    msg['Subject'] = 'location' + ': ' + subject
    msg.attach(MIMEText(body, 'plain'))
    text = msg.as_string()

    try:
        email_server = smtplib.SMTP('smtp.gmail.com', 587)
        email_server.starttls()
        email_server.login(server_email_address, server_email_password)
        email_server.sendmail(server_email_address, recipients, text)

    except Exception as e:
        print( e )
        log_event	( f'Exception Thrown - Send mail - {e}')

    finally:
        email_server.quit()



if __name__ == '__main__':
    # path = str(Path.cwd())
    path = '/home/x/CAP/monitor'
    file_name = 'ip.txt'
    path_file_name = Path(path, file_name)
    last_ip = get_last_known_ip(path_file_name)
    wan_ip = get_wan_ip()

    if last_ip != wan_ip:
        update_ip(path_file_name, wan_ip)
        base_path_remote = '/bayrvs/link'
        ftp(base_path_remote, path_file_name, file_name)   # This works when manually testing but crontab does not have the same pwd so you need to include the path.
        notify('CAP ALERT', 'CAP Server has new WAN IP.')
