import smtplib                          
smtpServer='smtp.gmail.com'      
fromAddr='vikas.derpdata@gmail.com'         
toAddr='vikas.derpdata@gmail.com'     
text= "This is a test of sending email from within Python."
server = smtplib.SMTP(smtpServer,25)
server.ehlo()
server.starttls()
server.sendmail(fromAddr, toAddr, text) 
server.quit()