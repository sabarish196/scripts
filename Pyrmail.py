import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(recipient, subject, body, relay_server, port):
    sender = 'your_email@example.com'  # Change this to your email address

    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = recipient
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(relay_server, port)
        server.sendmail(sender, recipient, msg.as_string())
        server.quit()
        print("Email sent successfully")
    except Exception as e:
        print("Failed to send email:", str(e))

if __name__ == "__main__":
    if len(sys.argv) != 6:
        print("Usage: python script.py recipient subject body relay_server port")
        sys.exit(1)
    
    recipient = sys.argv[1]
    subject = sys.argv[2]
    body = sys.argv[3]
    relay_server = sys.argv[4]
    port = int(sys.argv[5])
    
    send_email(recipient, subject, body, relay_server, port)
