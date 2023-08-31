import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Email configuration
sender_email = 'vikas.derpdata@gmail.com'
receiver_email = 'vikas.derpdata@gmail.com'
subject = 'Developer mode turned off'
message = 'Hiii !! The developer mode on your ERPNext site has been turned off.'

# Create the email
msg = MIMEMultipart()
msg['From'] = sender_email
msg['To'] = receiver_email
msg['Subject'] = subject
msg.attach(MIMEText(message, 'plain'))

# SMTP server configuration (example: open SMTP server)
smtp_server = 'smtp.gmail.com'
smtp_port = 25  # Use 465 for SSL or 587 for TLS

# Connect to the SMTP server
server = smtplib.SMTP(smtp_server, smtp_port)
server.starttls()  # Establish a secure TLS connection

# Send the email
server.sendmail(sender_email, receiver_email, msg.as_string())

# Quit the server
server.quit()

print("Email sent successfully!")