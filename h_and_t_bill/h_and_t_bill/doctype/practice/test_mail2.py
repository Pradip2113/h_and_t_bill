import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Email configuration
sender_email = 'vikas.derpdata@gmail.com'
receiver_email = 'vikas.derpdata@gmail.com'
subject = 'Developer mode turned off'
message = 'The developer mode on your ERPNext site has been turned off.'

# Create the email
msg = MIMEMultipart()
msg['From'] = sender_email
msg['To'] = receiver_email
msg['Subject'] = subject
msg.attach(MIMEText(message, 'plain'))

# SMTP server configuration
smtp_server = 'smtp.gmail.com'
smtp_port = 587  # Use 465 for SSL or 587 for TLS
smtp_username = 'vikas.derpdata@gmail.com'
smtp_password = 'dhnycuexqizsawip'

# Connect to the SMTP server
server = smtplib.SMTP(smtp_server, smtp_port)
server.starttls()  # For TLS encryption
# server = smtplib.SMTP_SSL(smtp_server, smtp_port)  # For SSL encryption

# Log in to the server
server.login(smtp_username, smtp_password)

# Send the email
server.sendmail(sender_email, receiver_email, msg.as_string())

# Quit the server
server.quit()

print("Email sent successfully!")
