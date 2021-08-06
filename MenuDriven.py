import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import getpass
import email
import imaplib
from email.header import decode_header
from email import message
from Crypto.PublicKey import RSA

print("---Login to SecureSecureEmail---")
#em = input("Enter EmailID:")
#passwd =  getpass.getpass("Enter Password:")

em = "bob.ca2.paul@gmail.com"
passwd = "bobpassword"
#em = "alice.ca2.paul@gmail.com"
#passwd = "alicepassword"

print(em+" "+passwd)


## Provide email and password to api to create session
session = smtplib.SMTP('smtp.gmail.com', 587)
session.starttls()

try:
	session.login(em,passwd)
except smtplib.SMTPAuthenticationError:
	print("Wrong Email Or Password")
	exit()

print("Login Successful!")

menu='''
Menu:
1. Send Email
2. Inbox
3. Key Exchange
4. Generate Key Pair for self (Using RSA)
'''

print(menu)

choice = input("Enter Choice:")


####### Generate PU PR key pair using RSA
if choice=='4':
	### Generate and save private key
	key = RSA.generate(2048)
	private_key = key.export_key()
	f = open("Keys/private.pem","wb")
	f.write(private_key)
	f.close()
	print("Private key Generated")


	### Generate and save Public Key
	public_key = key.publickey().export_key()
	f = open("Keys/public.pem","wb")
	f.write(public_key)
	f.close()
	print("Public key Generated")





####  Choice 3 To send request for new key

if choice=='3':
	ask = '''
	Choose Option:
	1. Request key
	2. Send key
	3. Store recieved keys
	Enter you choice:
	'''
	choice1 = input(ask)


	if choice1 == '1':
### logic to request key =>
		recieEmail = input("Enter Receiver's Emailid:")
		message = MIMEMultipart()
		message['From'] = em
		message['To'] = recieEmail
		message['Subject'] = 'SEND PUB KEY'
		msg = open("Keys/public.pem").read()
		message.attach(MIMEText(msg, 'plain'))
		text = message.as_string()
		session.sendmail(em, recieEmail, text)
		print("Key request sent!")
		print("Key will be recieved whenever requested party opens the request. Keep eyes on inbox.")
		

	#### Logic to Store Keys
	if choice1 == '3':
		M = imaplib.IMAP4_SSL("imap.gmail.com")
		# authenticate
		M.login(em, passwd)
		M.select("INBOX")
		typ, data = M.search(None, 'ALL')

		for num in data[0].split():
			#print(num)
			typ, data = M.fetch(num, '(RFC822)')
			msg = email.message_from_bytes(data[0][1])
			#print(msg)
			From, encoding = decode_header(msg.get("From"))[0]
			#print(From)
			subject, encoding = decode_header(msg["Subject"])[0]
			#print(subject)
			if subject == "PUB KEY" or subject == "SEND PUB KEY":
				##########Get message body
				if msg.is_multipart():
					# iterate over email parts
					for part in msg.walk():
						# extract content type of email
						content_type = part.get_content_type()
						content_disposition = str(part.get("Content-Disposition"))
						try:
						# get the email body
							body = part.get_payload(decode=True).decode()
						except:
							pass
						if content_type == "text/plain" and "attachment" not in content_disposition:
						# print text/plain emails and skip attachments
							print(body)
							#### Writing key into message
							f = open("Contacts/"+From+".pem","wb")
							f.write(body.encode())
							print("Key Saved for Email: "+From)
							if subject == "PUB KEY": M.store(num,'+Flags','\\Deleted')  #### Delete the email which shared the pub key
							
		
		M.close()






	#### Logic to Send PU key=>
	if choice1 == '2':
		M = imaplib.IMAP4_SSL("imap.gmail.com")
		# authenticate
		M.login(em, passwd)
		M.select("INBOX")
		typ, data = M.search(None, 'ALL')

		for num in data[0].split():
			#print(num)
			typ, data = M.fetch(num, '(RFC822)')
			msg = email.message_from_bytes(data[0][1])
			#print(msg)
			From, encoding = decode_header(msg.get("From"))[0]
			#print(From)
			subject, encoding = decode_header(msg["Subject"])[0]
			#print(subject)
			if subject == "SEND PUB KEY":
				#session = smtplib.SMTP('smtp.gmail.com', 587) 
				#session.starttls()
				#session.login(em, passwd)
				#print("SMTP Login Successful")
				msg = open("Keys/public.pem").read()
				#### Craft the email
				message = MIMEMultipart()
				message['From'] = em
				message['To'] = From ##Requester
				message['Subject'] = "PUB KEY"
				message.attach(MIMEText(msg, 'plain'))
				text = message.as_string()
				session.sendmail(em,From,text) ## Send Email
				print("Public Key Sent to Email: "+From)
				M.store(num,'+Flags','\\Deleted')

		






#### Choice 2 Inbox
#.if choice == '2':





### Choice 3 Send mail
if choice == '1':
	recieEmail = input("Enter Email:")
	subject = input("Enter Subject:")
	msg = input("Enter Message:")

	#### Craft the email
	message = MIMEMultipart()
	message['From'] = em
	message['To'] = recieEmail
	message['Subject'] = subject
	message.attach(MIMEText(msg, 'plain'))

	### Send Email
	text = message.as_string()
	session.sendmail(em,recieEmail, text)










session.quit()