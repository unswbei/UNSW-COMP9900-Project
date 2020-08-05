#!/usr/bin/python3
import smtplib, yaml
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header

class SMTP:
    def __init__(self):
        """Implemented smtp class"""
        f = open('smtp.config', 'r', encoding='utf-8')
        config = yaml.load(f.read(), Loader=yaml.FullLoader)
        self.smtp_host = config['SMTP']['Host']
        self.smtp_port = int(config['SMTP']['Port'])
        self.smtp_user = config['SMTP']['User']
        self.smtp_pass = config['SMTP']['Pass']
        self.sender = config['SMTP']['Sender']
        self.reconnect()

    def send_email_plain(self, receiver, content, subject):
        """Send plain text email
        Param:
        receiver - receiver(s) of email
        content - major content of email
        subject - subject of email
        Return:
        Boolean if send success
        """
        message = MIMEText(content, 'plain', 'utf-8')
        return self.send_out(receiver, subject, message)

    def send_email_html(self, receiver, content, subject):
        """Send html text email
        Param:
        receiver - receiver(s) of email
        content - major content of email
        subject - subject of email
        Return:
        Boolean if send success
        """
        message = MIMEText(content, 'html', 'utf-8')
        return self.send_out(receiver, subject, message)

    def send_out(self, receiver, subject, message):
        """General send out email function
        Param:
        receiver - receiver(s) of email
        message - a MIMEText object to send out
        subject - subject of email
        Return:
        Boolean if send success
        """
        message['From'] = Header(self.sender)
        message['To'] = Header(receiver)
        message['Subject'] = Header(subject)
        try:
            self.server.sendmail(self.sender, receiver, message.as_string())
            print("Email send to " + str(receiver) + " success")
            return True
        except smtplib.SMTPException as e:
            print(f"Send email to {str(receiver)} failed, retry")
            self.reconnect()
            try:
                self.server.sendmail(self.sender, receiver, message.as_string())
                print(f"Send email to {str(receiver)} success in retry 1")
            except smtplib.SMTPException as e:
                print(f"Resend to {str(receiver)} failed.")
            return False
            
    def reconnect(self):
        """Connect/Reconnect to smtp server"""
        self.server = smtplib.SMTP_SSL(self.smtp_host, self.smtp_port)
        self.server.login(self.smtp_user, self.smtp_pass)
