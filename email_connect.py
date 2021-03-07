import smtplib, ssl, email
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import yaml


def send_email(filenames, password):
    # Gets config info so we can access the user email address
    config = {}
    try:
        config = yaml.safe_load(open("config.yml", "r"))
    except FileNotFoundError as e:
        print(
            "Error: No config.yml found, using placeholder values, which will not work!"
        )
    sender = config.get("sender")
    recipient = config.get("email")
    subject = "NOTIFICATION FROM SECURITY SERVICE"
    body = (
        "Dear User, \n\nThis message is to notify you that your "
        + "security system has detected movement in front "
        + "of your camera. Please find attached photos of the incident "
        + "that was detected. \nPlease do not reply to this message as "
        + "this email is not monitored.\n\nThank you, \nTeam Little Brother "
    )

    message = MIMEMultipart()
    message["From"] = sender
    message["To"] = recipient
    message["Subject"] = subject

    message.attach(MIMEText(body, "plain"))  # attach body to email

    if type(filenames) == str:  # if there is only one file
        fp = open(filenames, "rb")
        image = MIMEImage(fp.read())
        fp.close()
        image.add_header("Content-ID", "<image1>")  # attach image to email
        message.attach(image)
    elif type(filenames) == list:  # if there are multiple files
        for i in range(0, len(filenames)):
            fp = open(filenames[i], "rb")
            image = MIMEImage(fp.read())
            fp.close()
            image.add_header("Content-ID", "<image1>")  # attach each image to email
            message.attach(image)

    text = message.as_string()

    # Creating a server object from the smtplib library on port 587.
    # Port 587 is the TCP port that most modern email clients use.

    # Server uses SMTP protocol.

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        try:  # if login attempt fails then an exception is thrown
            server.login(sender, password)
        except:
            print("Incorrect password, email failed to send.")
            return
        print("Login was a success. ")
        server.sendmail(sender, recipient, text)
        print("Email sent to email specified.")
