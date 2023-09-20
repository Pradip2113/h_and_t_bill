# import smtplib                          
# smtpServer='smtp.gmail.com'      
# fromAddr='vikas.derpdata@gmail.com'         
# toAddr='vikas.derpdata@gmail.com'     
# text= "This is a test of sending email from within Python."
# server = smtplib.SMTP(smtpServer,25)
# server.ehlo()
# server.starttls()
# server.sendmail(fromAddr, toAddr, text) 
# server.quit()

# import smtplib
# receiver = 'vikas.derpdata@gmail.com'
# sender = 'vikas.derpdata@gmail.com'
# smtp = smtplib.SMTP('25')

# subject = 'test'
# body = 'testing plain text message'
# msg = 'subject: ' + subject + ' \n\n' + body

# smtp.sendmail('sender', receiver, msg)