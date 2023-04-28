""" monitor.py is executed from a local monitor / development server
             / backup server that monitors the live server.
    Monitors via local ip.
    Monitors router's port forwarding
"""



import os
import sys
import json
import time
import ftplib
import requests
import smtplib
import credentials as c
from pathlib import Path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from ftplib import FTP, error_perm



def get_wan_ip():
    ip = requests.get('https://api.ipify.org').content.decode('utf8')
    print(f'Live ip: {ip}')
    return ip

def local_ip_alive():
    url = f'http://{c.server_ip}:{c.server_port}/alive'
    # url = f'http://{c.samstock_ip}:{c.samstock_port}/alive'
    response = requests.get(url)
    alive = response.json()['alive']
    print(f'local ip alive: {alive}')
    return alive

def port_forwarding(wan_ip):
    # url = f'http://{wan_ip}'
    url = f'http://{wan_ip}:{c.server_port}/alive'
    r = None
    try:
        r = requests.get(url, params={})
    except requests.exceptions.RequestException as e:
        print(e)
        return False

    # if r.status_code == 200:
    #     return True
    alive = r.json()['alive']
    print(f'wan ip -> port forwarding alive: {alive}')
    return alive


def notify(subject, body):
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    print('notify')
    msg = MIMEMultipart()
    msg['From'] = c.server_email_address
    msg['To'] =  ", ".join( c.recipients )
    msg['Subject'] = 'location' + ': ' + subject
    msg.attach(MIMEText(body, 'plain'))
    text = msg.as_string()

    try:
        email_server = smtplib.SMTP('smtp.gmail.com', 587)
        email_server.starttls()
        email_server.login(c.server_email_address, c.server_email_password)
        email_server.sendmail(c.server_email_address, c.recipients, text)

    except Exception as e:
        print( e )
        log_event	( f'Exception Thrown - Send mail - {e}')

    finally:
        email_server.quit()


if __name__ == '__main__':
    wan_ip = get_wan_ip()
    alive = local_ip_alive()
    if not alive:
        notify('CAP ALERT', 'Server is MIA.')

    alive = port_forwarding(wan_ip)
    if not alive:
        notify('CAP ALERT', 'Router denied port forwarding.')
