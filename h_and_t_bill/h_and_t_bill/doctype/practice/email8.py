import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json
# import schedule
# import time

SENDER_EMAIL = 'vikas.derpdata@gmail.com'
RECEIVER_EMAIL = 'vikas.derpdata@gmail.com'
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SMTP_USERNAME = 'vikas.derpdata@gmail.com'
SMTP_PASSWORD = 'dhnycuexqizsawip' 

# def get_site_name():
#     with open('/home/erpadmin/bench05-dev-vppl/sites/deverpvppl.erpdata.in/site_config.json', 'r') as config_file:
#         config = json.load(config_file)
#         site_name = config.get('site_name', 'deverpvppl.erpdata.in')
#         return site_name

file_path = '/home/erpadmin/bench05-dev-vppl/sites/deverpvppl.erpdata.in/site_config.json'
path_parts = file_path.split('/')

if len(path_parts) >= 2:
    site_name = path_parts[-2]
    print("Site Name:", site_name)
else:
    print("Could not determine the site name from the file path.")

def send_email():
    subject = 'Important Notification: Developer Mode Status'
    
    try:
        with open('/home/erpadmin/bench05-dev-vppl/sites/deverpvppl.erpdata.in/site_config.json', 'r') as config_file:
            config = json.load(config_file)
            developer_mode = config.get('developer_mode', 0)

            if developer_mode:
                status = 'ON'
            else:
                status = 'OFF'

            html = f"""\
                <html>
                <head></head>
                <body>
                    <p style='font-size:16px;'>
                    Site Name - {site_name}.
                    </p>
                    <p style='font-size:16px;'>
                    Developer Mode Status - <b>{status}</b>.
                    </p>
                </body>
                </html>
                """
    except FileNotFoundError as e:
        print(f"File not found: {e}")
        return

    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL
    msg['Subject'] = subject
    msg.attach(MIMEText(html, 'html'))

    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(SMTP_USERNAME, SMTP_PASSWORD)
    server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
    server.quit()

# schedule.every(1).seconds.do(send_email)

# while True:
#     schedule.run_pending()
#     time.sleep(1)
