import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import getpass
import email
import imaplib
from email.header import decode_header
from email import message

print("---Login to SecureSecureEmail---")
email = input("Enter EmailID:")
passwd =  getpass.getpass("Enter Password:")

print(email+" "+passwd)

## Provide email and password to api to create session
session = smtplib.SMTP('smtp.gmail.com', 587)
session.starttls()

try:
	session.login(email,passwd)
except smtplib.SMTPAuthenticationError:
	print("Wrong Email Or Password")
	exit()

print("Login Successful!")

menu='''
Menu:
1. Send Email
2. Inbox
3. Key Exchange
'''

print(menu)

choice = input("Enter Choice:")

####  Choice 3 To send request for new key

if choice=='3':
	### logic to request key =>
	recieEmail = input("Enter Receiver's Emailid:")
	message = MIMEMultipart()
	message['From'] = email
	message['To'] = recieEmail
	message['Subject'] = 'SEND PUB KEY'
	text = message.as_string()
	flag=0
	try:
		session.sendmail(email, recieEmail, text)
		flag=1
	except:
		print("Error Occured while sending request")
		flag=0	

	if flag==1:
		print("Key request sent!")
		print("Key will be recieved whenever requested party opens the request")

	#### Logic to store recieved key=>
	# 
	# 	




#### Choice 2 Inbox
#if choice == '2':





### Choice 3 Send mail
if choice == '1':
	recieEmail = input("Enter Email:")
	subject = input("Enter Subject:")
	msg = input("Enter Message:")

	#### Craft the email
	message = MIMEMultipart()
	message['From'] = email
	message['To'] = recieEmail
	message['Subject'] = subject
	message.attach(MIMEText(msg, 'plain'))

	### Send Email
	text = message.as_string()
	session.sendmail(email,recieEmail, text)










session.quit()