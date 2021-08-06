import email
import imaplib
import email
from email.header import decode_header
from email import message

username='bob.ca2.paul@gmail.com'
password='bobpassword'


M = imaplib.IMAP4_SSL("imap.gmail.com")
# authenticate
M.login(username, password)

M.select("INBOX")
typ, data = M.search(None, 'ALL')

#typ, data = M.fetch('5', '(RFC822)')
print("="*100)
for num in data[0].split():
	print(num)
	typ, data = M.fetch(num, '(RFC822)')

	msg = email.message_from_bytes(data[0][1])

	#print(msg)

	subject, encoding = decode_header(msg["Subject"])[0]

	print(subject)

	From, encoding = decode_header(msg.get("From"))[0]

	print(From)
	print("-"*100)
print("="*100)

selectEmail = input("Enter Email Number to view:")
typ, data = M.fetch(selectEmail, '(RFC822)')
msg = email.message_from_bytes(data[0][1])
subject, encoding = decode_header(msg["Subject"])[0]
print(subject)
From, encoding = decode_header(msg.get("From"))[0]
print(From)

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

