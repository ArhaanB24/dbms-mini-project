import smtplib
import os
from email.message import EmailMessage
mail_lst = ["naitechh@gmail.com"] # add list of celebrity emails 
# can import from file but need to write extra code
def sendmail(name,mail,message):
    msg = EmailMessage()
    s = smtplib.SMTP("smtp.gmail.com",587)
    s.starttls()
    s.login("notesportalofficial@gmail.com",os.environ.get("EMAIL_KEY"))
    msg['Subject'] = "Welcome User"
    msg['From'] = "notesportalofficial@gmail.com"
    msg['To'] = mail
    msg.set_content(
        message,
        subtype="html"
    )
    s.send_message(msg)
    print("message sent")
    s.quit()