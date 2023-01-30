import requests
from time import ctime, sleep
import smtplib

DEFAULT_INTERVAL = 30
DEFAULT_SMTP_URL = "smtp.gmail.com"
DEFAULT_SMTP_PORT = 587
DEFAULT_SUBJECT = "Webpage Content Changed"
DEFAULT_MESSAGE = """Subject: {s}

The contents of the webpage have changed! {u}

Previous content:
{p}

Current content:
{c}"""

def monitor(url: str, sender_email: str, sender_password: str,
            recipient_email=None, interval=DEFAULT_INTERVAL,
            subject=DEFAULT_SUBJECT, message=DEFAULT_MESSAGE,
            smtp_url=DEFAULT_SMTP_URL, smtp_port=DEFAULT_SMTP_PORT):

    if recipient_email is None:
        recipient_email = sender_email

    previous_content = None

    def send_notification(previous_content, current_content):
        msg = message.format(s=subject,
                                 p=previous_content,
                                 c=current_content,
                                 u=url
                                ).encode("utf-8")
        try:
            with smtplib.SMTP(smtp_url, smtp_port) as smtp:
                smtp.ehlo()
                smtp.starttls()
                smtp.ehlo()
                smtp.login(sender_email, sender_password)
                smtp.sendmail(sender_email, recipient_email, msg)
        except Exception as e:
            print(f"Error sending email: {e}")

    print(f"{ctime()}: started monitoring {url}.")
    while True:
        print(f"{ctime()}: downloading page.")
        response = requests.get(url)
        current_content = response.text
        if previous_content and previous_content != current_content:
            print(f"{ctime()}: change detected.")
            send_notification(previous_content, current_content)
        previous_content = current_content
        sleep(interval * 60) # wait for `interval` minutes
