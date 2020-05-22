import smtplib, ssl

port = 587  # For starttls
smtp_server = "smtp.gmail.com"
sender_email = "youmail@gmail.com"
receiver_email = "reciever@gmail.com"
password = 'yourpassword'
message = """\
Subject: Final Model Build 

Pull it from GitHub along with history file, that is saved using pickle module


"""

context = ssl.create_default_context()
with smtplib.SMTP(smtp_server, port) as server:
    server.ehlo()  # Can be omitted
    server.starttls(context=context)
    server.ehlo()  # Can be omitted
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message)


#upload the model on google drive and share the link with mail
