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


import yagmail
import sys

def send_email(sender_email, sender_password, recipient_email, subject, body, relay_server, port):
    # Set up yagmail with relay server and port
    yag = yagmail.SMTP(
        user=sender_email,
        password=sender_password,
        host=relay_server,
        port=port
    )

    # Send the email
    yag.send(
        to=recipient_email,
        subject=subject,
        contents=body
    )

    print("Email sent successfully")

# Example usage:
if __name__ == "__main__":
    if len(sys.argv) != 7:
        print("Usage: python script.py sender_email sender_password recipient_email subject body relay_server port")
        sys.exit(1)

    sender_email = sys.argv[1]
    sender_password = sys.argv[2]
    recipient_email = sys.argv[3]
    subject = sys.argv[4]
    body = sys.argv[5]
    relay_server = sys.argv[6]
    port = sys.argv[7]

    send_email(sender_email, sender_password, recipient_email, subject, body, relay_server, port)

