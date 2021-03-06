import smtplib, ssl

sender = "camera.notifier99@gmail.com"
recipient = "mattmione37@gmail.com"

message = "Hello! " # This will have to change based on the context when we send.

password = str(input("Type your password: "))

# Creating a server object from the smtplib library on port 587. 
# Port 587 is the TCP port that most modern email clients use.

# Server uses SMTP protocol.
server = smtplib.SMTP('smtp.gmail.com',587);

# Using TLS encryption to send the emails, uing the starttls() method.
# First we need to check if the TLS encryption has happened using ehlo()
# However this is done implicitly by startls() if the server requires it. 
server.ehlo()
server.starttls();
server.ehlo()

server.login(sender,password);

print("Login was a success. ");
server.sendmail(sender, recipient, message);

print("Email sent to email specified.");