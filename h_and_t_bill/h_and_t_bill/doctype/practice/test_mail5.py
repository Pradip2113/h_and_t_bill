# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# import base64
# import os

# from google.auth import exceptions
# from google.oauth2 import service_account

# # Email configuration
# sender_email = 'vikas.derpdata@gmail.com'
# receiver_email = 'vikas.derpdata@gmail.com'
# subject = 'Developer mode turned off'
# message = 'Hiii !! The developer mode on your ERPNext site has been turned off.'

# # Create the email
# msg = MIMEMultipart()
# msg['From'] = sender_email
# msg['To'] = receiver_email
# msg['Subject'] = subject
# msg.attach(MIMEText(message, 'plain'))

# # SMTP server configuration
# smtp_server = 'smtp.gmail.com'
# smtp_port = 587  # Use 465 for SSL or 587 for TLS

# # Load the credentials from a JSON service account key file
# credentials_path = 'path/to/your/service-account-key.json'  # Update this path
# credentials = service_account.Credentials.from_service_account_file(credentials_path, scopes=['https://www.googleapis.com/auth/gmail.send'])

# # Use the credentials to authorize an email sending
# try:
#     auth_token, _ = credentials._make_authorization_grant_assertion()
# except exceptions.GoogleAuthError as e:
#     print(f"Authorization failed: {e}")
#     exit()

# # Connect to the SMTP server
# server = smtplib.SMTP(smtp_server, smtp_port)
# server.starttls()  # Establish a secure TLS connection

# # Authenticate with OAuth 2.0
# server.docmd('AUTH', 'XOAUTH2 ' + base64.b64encode(auth_token.encode()).decode())

# # Send the email
# server.sendmail(sender_email, receiver_email, msg.as_string())

# # Quit the server
# server.quit()

# print("Email sent successfully!")
