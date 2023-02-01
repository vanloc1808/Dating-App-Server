import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SENDER_ADDRESS = ''
SENDER_PASSWORD = ''

def send_password_recovery_mail(receiver_email, recovery_key):
    subject = 'Password recovery email'
    mail_content = 'Your key for recovering password in Dating App is ' + recovery_key + '. Your key will be valid for 15 minutes'
    
    message = MIMEMultipart()
    message['From'] = SENDER_ADDRESS
    message['To'] = receiver_email
    message['Subject'] = 'Dating app password recovery key'

    session = smtplib.SMTP('smtp.gmail.com', 587) # use Gmail with port
    session.starttls() # enable security
    session.login(SENDER_ADDRESS, SENDER_PASSWORD) # login with mail_id and password
    
    text = message.as_string()

    session.sendmail(SENDER_ADDRESS, receiver_email, text)
    session.quit()

    print('Password recovery mail sent')
