

import aiosmtplib

import asyncio

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from .prepare_html_file import prepare_html_file

import os

from typing import List

from dotenv import load_dotenv

load_dotenv(override=True)


MAIL_USERNAME = os.getenv("MAIL_USERNAME", "").strip()
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", "").strip()


async def send_email_msg(
        email:str, reason:str, link:str|None=None, max_retries:int=3,
        user_name:str|None=None, msg:str|None=None
) -> None:

    """
    emails sending reasons:\n
    1.submit_contact_us_form\n
    2.reset_password\n
    3.send_reply_email\n
    4.notification_email\n
    """

    message = MIMEMultipart()
    message["From"] = MAIL_USERNAME
    message["To"] = email

    if reason == "submit_contact_us_form":

        message["Subject"] = f"Message From {email.split("@")[0]}"

        file_path = "helpers/email_service/assets/submit_contact_us_form.html"
        html_content = await prepare_html_file(
            link, email, file_path, reason, user_name, msg
        )

    elif reason == "send_reply_email":

        message["Subject"] = f"Reply From Developer Seth"

        file_path = "helpers/email_service/assets/send_reply_email.html"
        html_content = await prepare_html_file(
            link, email, file_path, reason, user_name, msg
        )

    else:
        html_content=""
    
    #message.attach(MIMEText("plain_text", "plain"))
    message.attach(MIMEText(html_content, "html", "utf-8"))
    
    for retry in range(max_retries):
        try:
            await aiosmtplib.send(
                message,
                sender=MAIL_USERNAME,
                recipients=[email],
                hostname="smtp.gmail.com",
                port=587,
                password=MAIL_PASSWORD,
                username=MAIL_USERNAME,
                use_tls=False,
                start_tls=True,
                timeout=10,
            )
            print("Email sent successfully.")

            return
        except Exception as e:
            if retry == max_retries - 1:

                print(f"Error sending email after {max_retries} retries")
                print(f"Error = {e}")
            else:
                print(f"Error sending email. Retrying... ({retry + 1}/{max_retries})")
                print(f"Error = {e}")
                await asyncio.sleep(2**retry)  # Exponential backoff