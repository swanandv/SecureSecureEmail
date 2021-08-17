# SecureSecureEmail
Python app to send emails using Gmail, encrypted with AES. 

After getting the script on the machine, create two folders in the same folder from where you will run the program.
Folder names should be as follows (Case-Sensitive):
1. Keys
2. Contacts

Keys will store your own Public and Private Keys created using RSA.
Contacts will store Public Keys of recipients.

After that, run the script using python.

> python SecureSecureEmail.py 

Step1: Create the Keys for yourself using option no 4.

Step2: Send Email. Enter the recipient's email-id. If the key of the recipient is already in Contacts folder then it will run smooth. If not, it will send key request to the recipient.

Step3: If you see in your Inbox the email with subject- "PUB KEY" then you have recieved Public Key of the person you sent request to. You can save this key using option 3. Key Exchange.

Step4: By this point, Key Exchange have been completed. Both the parties can exchange emails.



