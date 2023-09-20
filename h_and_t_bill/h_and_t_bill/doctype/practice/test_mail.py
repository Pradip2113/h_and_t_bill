# Assuming the custom script is attached to a specific document type

# import frappe
# def send_email_if_developer_mode(doc):
#         site_config = frappe.get_site_config()
#         developer_mode = site_config.get("developer_mode")
#         if developer_mode:
#             email_content = "This is the email content."
            
#             frappe.sendmail(
#                 recipients=["vikas.derpdata@gmail.com"],
#                 subject="Regarding developer mode",
#                 message=email_content
#             )

# def send_email_if_developer_mode(doc):
#     # Check if developer mode is active (pseudocode)
#     if developer_mode_is_active():
#         email_content = "Developer Mode currently ON."
        
#         frappe.sendmail(
#             recipients=["vikas.derpdata@gmail.com"],
#             subject="Regarding developer mode",
#             message=email_content
#         )


# import requests
# import json

# def send_email(site_url, email_to, email_subject, email_body):
#   """Sends an email notification when developer mode is turned off on an ERPNext site.

# #   Args:
# #     site_url: deverpvppl.erpdata.in
# #     email_to: vikas.derpdata@gmail.com
# #     email_subject: Regarding developer mode.
# #     email_body: The developer mode on your ERPNext site has been turned off..
# #   """

#   payload = {
#     "email_to": email_to,
#     "email_subject": email_subject,
#     "email_body": email_body,
#   }

#   response = requests.post(site_url + "/api/send_email", json=payload)

#   if response.status_code == 200:
#     print("Email sent successfully.")
#   else:
#     print("Error sending email.")

# if __name__ == "__main__":
#   site_url = "http://deverpvppl.erpdata.in/app"
#   email_to = "vikas.derpdata@gmail.com"
#   email_subject = "Developer mode turned off"
#   email_body = "The developer mode on your ERPNext site has been turned off."

#   send_email(site_url, email_to, email_subject, email_body)


# import requests
# import json

# def send_email(site_url, email_to, email_subject, email_body):
#     """Sends an email notification when developer mode is turned off on an ERPNext site.

#     Args:
#         site_url: http://deverpvppl.erpdata.in/app
#         email_to: vikas.derpdata@gmail.com
#         email_subject: The subject of the email notification.
#         email_body: The body of the email notification.
#     """

#     payload = {
#         "email_to": email_to,
#         "email_subject": email_subject,
#         "email_body": email_body,
#     }

#     try:
#         response = requests.post(site_url + "/api/send_email", json=payload)

#         if response.status_code == 200:
#             print("Email sent successfully.")
#         else:
#             print(f"Error sending email. Status code: {response.status_code}")
#     except requests.exceptions.RequestException as e:
#         print(f"An error occurred: {e}")

# if __name__ == "__main__":
#     site_url = "http://deverpvppl.erpdata.in/app"
#     email_to = "vikas.derpdata@gmail.com"
#     email_subject = "Developer mode turned off"
#     email_body = "The developer mode on your ERPNext site has been turned off."

#     send_email(site_url, email_to, email_subject, email_body)

# import smtplib
# from email.message import EmailMessage

# def send_email(email_to, email_subject, email_body):
#   """Sends an email notification when developer mode is turned off on an ERPNext site.

#   Args:
#     email_to: The email address to send the notification to.
#     email_subject: The subject of the email notification.
#     email_body: The body of the email notification.
#   """

#   message = EmailMessage()
#   message["From"] ="noreply@gmail.com"
#   message["To"] = email_to
#   message["Subject"] = email_subject
#   message["Body"] = email_body

#   smtp_server = "smtp.gmail.com"
#   smtp_port = 587
#   smtp_username = "vikas.derpdata@gmail.com"
#   smtp_password = "dhnycuexqizsawip"

#   with smtplib.SMTP(smtp_server, smtp_port) as smtp:
#     smtp.ehlo()
#     smtp.starttls()
#     smtp.login(smtp_username, smtp_password)
#     smtp.send_message(message)

# if __name__ == "__main__":
#   email_to = "vikas.derpdata@gmail.com"
#   email_subject = "Developer mode turned off"
#   email_body = "The developer mode on your ERPNext site has been turned off.".encode()

#   send_email(email_to, email_subject, email_body)
