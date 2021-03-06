import smtplib, ssl

password = input(str("Type your password and press enter: "))

# Creating a server object from the smtplib library on port 587. 
# Port 587 is the TCP port that most modern email clients use.

# Server uses SMTP protocol.
server = smtplib.SMTP('smtp.gmail.com',587);
server.starttls();
server.login("camera.notifier99@gmail.com",password);

# 
print("Login was a success. ");
server.sendmail("camera.notifier99@gmail.com", "mattmione37@gmail.com", "Hello world. ");

print("Email sent to email specified. ");