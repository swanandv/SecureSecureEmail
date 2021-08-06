import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

sender_address = 'alice.ca2.paul@gmail.com'
sender_pass = 'alicepassword'

session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
session.starttls() #enable security
session.login(sender_address, sender_pass) #login with mail_id and password

print("Login Successful")



recieEmail = input("Enter Email:")

f = open("keys/public.pem").read()

msg = f

#### Craft the email
message = MIMEMultipart()
message['From'] = sender_address
message['To'] = recieEmail
message['Subject'] = "PUB KEY"
message.attach(MIMEText(msg, 'plain'))

### Send Email
text = message.as_string()
session.sendmail(sender_address,recieEmail, text)

print("Public Key Sent")