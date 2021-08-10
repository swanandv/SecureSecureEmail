import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import getpass
import email
import imaplib
from email.header import decode_header
from email import message
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP

print("---Login to SecureSecureEmail---")
em = input("Enter EmailID:")
passwd =  getpass.getpass("Enter Password:")

#print(em+" "+passwd)


## Provide email and password to api to create session
session = smtplib.SMTP('smtp.gmail.com', 587)
session.starttls()

try:
	session.login(em,passwd)
except smtplib.SMTPAuthenticationError:
	print("Wrong Email Or Password")
	exit()

print("Login Successful!")

while(True):

	menu='''\n\n\n
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
		flag=0 ## Flag to check key exchange activity
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
			if subject == "SEND PUB KEY" or subject == "FIN KEY XCH":
				flag=1
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
							#### Writing key into File
							f = open("Contacts/"+From+".pem","wb")
							f.write(body.encode())
							print("Key Saved for Email: "+From)
							print("Key exchange finish. Now you can Send Messages to "+From)
							

			if subject == "SEND PUB KEY":
				flag=1
				#### Key is saved in privious section. Now sending public key.
				msg = open("Keys/public.pem").read()
				message = MIMEMultipart()
				message['From'] = em
				message['To'] = From ##Requester
				message['Subject'] = "FIN KEY XCH"
				message.attach(MIMEText(msg, 'plain'))
				text = message.as_string()
				session.sendmail(em,From,text) ## Send Email
				print("Public Key Sent to Email: "+From)
				print("Key exchange finish. Now you can Send Messages to "+From)

			#### Delete Key exchange noice from Inbox
			if subject == "SEND PUB KEY" or subject == "FIN KEY XCH": M.store(num,'+Flags','\\Deleted')  #### Delete the email which shared the pub key					
		M.close()
		if flag == 0: print("No key exchanges pending.")



		




	#### Choice 2 Inbox
	if choice == '2':
		M = imaplib.IMAP4_SSL("imap.gmail.com")
		M.login(em, passwd)

		M.select("INBOX")
		typ, data = M.search(None, 'ALL')
		print("="*100)
		for num in data[0].split():
			print("SNo. "+num.decode())
			typ, data = M.fetch(num, '(RFC822)')
			msg = email.message_from_bytes(data[0][1])
			#print(msg)
			subject, encoding = decode_header(msg["Subject"])[0]
			From, encoding = decode_header(msg.get("From"))[0]
			print("Subect: "+subject)
			print("From: "+From)
			print("-"*100)
		print("="*100)

		selectEmail = input("Enter Email Number to view (q for quit):")
		if selectEmail == "q": continue
		typ, data = M.fetch(selectEmail, '(RFC822)')
		msg = email.message_from_bytes(data[0][1])
		subject, encoding = decode_header(msg["Subject"])[0]
		print(subject)
		From, encoding = decode_header(msg.get("From"))[0]
		print(From)

		# iterate over email parts
		for part in msg.walk():
			content_type = part.get_content_type()
			content_disposition = str(part.get("Content-Disposition"))
			try:
				body = part.get_payload(decode=True)
			except:
				pass
			if content_type == "text/plain" and "attachment" not in content_disposition:
				#print(body)
				################## DECRYPTION #################################################
				private_key = RSA.import_key(open("Keys/private.pem").read())
				####Slice the byte stream
				enc_session_key = body[:private_key.size_in_bytes()]
				nonce = body[private_key.size_in_bytes():private_key.size_in_bytes()+16]
				tag = body[private_key.size_in_bytes()+16:private_key.size_in_bytes()+16+16]
				ciphertext = body[private_key.size_in_bytes()+16+16:]	
				#### RSA decrypt
				cipher_rsa = PKCS1_OAEP.new(private_key)
				session_key = cipher_rsa.decrypt(enc_session_key)
				#### AES decrypt	
				cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
				data = cipher_aes.decrypt_and_verify(ciphertext, tag)
				print("\nDecrypted Message:\n")
				print(data.decode("utf-8"))
				print("\n\n\n")




		





	### Choice 1 Send mail
	if choice == '1':
		rec_email = input("Enter Email:")
		## Check if keys are there for the entered emailid if yes then read recipients pub key
		try:
			recipient_key = RSA.import_key(open("Contacts/"+rec_email+".pem").read())
		except FileNotFoundError:
			yn = input("Entered Email is not in your Contacts. Send Key Exchange Request (Y/N)?")
			if yn == "Y" or yn == "y": 
				##Send request of Pub key
				rec_email = input("Enter Receiver's Emailid:")
				message = MIMEMultipart()
				message['From'] = em
				message['To'] = rec_email
				message['Subject'] = "SEND PUB KEY"
				msg = open("Keys/public.pem").read()
				message.attach(MIMEText(msg, 'plain'))
				text = message.as_string()
				session.sendmail(em, rec_email, text)
				print("Key exchange request sent to "+rec_email)
				continue
			elif yn == "N" or yn == "n":
				continue

		subject = input("Enter Subject:")
		msg = input("Enter Message:").encode("utf-8")

		#### Craft the email
		message = MIMEMultipart()
		message['From'] = em
		message['To'] = rec_email
		message['Subject'] = subject

		########### ENCRYPTION #############################
		session_key = get_random_bytes(16)
		cipher_rsa = PKCS1_OAEP.new(recipient_key)
		enc_session_key = cipher_rsa.encrypt(session_key)

		cipher_aes = AES.new(session_key, AES.MODE_EAX)
		ciphertext, tag = cipher_aes.encrypt_and_digest(msg)

		body = enc_session_key + cipher_aes.nonce + tag + ciphertext

		message.attach(MIMEText(body, 'plain','utf-8'))

		### Send Email
		text = message.as_string()

		print("\n\n"+text)
		session.sendmail(em,rec_email, text)
		print("Encrypted Email Sent!")










session.quit()