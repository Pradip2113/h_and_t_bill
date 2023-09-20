import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import json
import schedule
import time


def get_site_name():
  with open('/home/erpadmin/bench05-dev-vppl/sites/deverpvppl.erpdata.in/site_config.json', 'r') as config_file:
    config = json.load(config_file)
    site_name = config.get('site_name', 'deverpvppl.erpdata.in')
    return site_name
print(get_site_name())


sender_email = 'vikas.derpdata@gmail.com'
receiver_email = 'vikas.derpdata@gmail.com'
subject = 'Important Notification: Developer Mode Status'
try:
    with open('/home/erpadmin/bench05-dev-vppl/sites/deverpvppl.erpdata.in/site_config.json', 'r') as config_file:  
        config = json.load(config_file)
        developer_mode = config.get('developer_mode', 0)
        if developer_mode:
            html = """\
                    <html>
                    <head></head>
                    <body>
                     <p style='font-size:16px;'>
                        Site Name - """+ get_site_name() + """ .
                        </p>
                        <p style='font-size:16px;'>
                        Developer Mode Status - <b>ON</b>.
                        </p>
                    </body>
                    </html>
                    """
             
        else:
            html = """\
                    <html>
                    <head></head>
                    <body>
                     <p style='font-size:16px;'>
                        Site Name - """+ get_site_name() + """ .
                        </p>
                        <p style='font-size:16px;'>
                        Developer Mode Status - <b>OFF</b>.
                        </p>
                    </body>
                    </html>
                    """
except FileNotFoundError:
    frappe.msgprint("File not found: site_config.json")

msg = MIMEMultipart()
msg['From'] = sender_email
msg['To'] = receiver_email
msg['Subject'] = subject
# msg.attach(MIMEText(message, 'plain'))
msg.attach(MIMEText(html, 'html'))

smtp_server = 'smtp.gmail.com'
smtp_port = 587  

username = 'vikas.derpdata@gmail.com'
password = 'dhnycuexqizsawip'

server = smtplib.SMTP(smtp_server, smtp_port)
server.starttls()  
server.login(username, password)
server.sendmail(sender_email, receiver_email, msg.as_string())
server.quit()

schedule.every(1).seconds.do(sendmail) 
while True:
    schedule.run_pending()
    time.sleep(1)
    
print("Email sent successfully!")
