import smtplib
from smtplib import SMTP
from email.message import EmailMessage
def sendmail(to,subject,body):
    server = smtplib.SMTP_SSL('smtp.gmail.com',465)
    server.login('srinikhilkomatineni357@gmail.com', 'oida yoku trbb hlxb')
    msg = EmailMessage()
    msg['From'] = 'srinikhilkomatineni357@gmail.com'
    msg['Subject'] = subject
    msg['To'] = to
    msg.set_content(body)
    server.send_message(msg)
    server.quit()