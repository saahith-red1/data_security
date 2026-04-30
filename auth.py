import random
import smtplib
from email.mime.text import MIMEText

from config import SMTP_SENDER_EMAIL, SMTP_APP_PASSWORD


def generate_code() -> str:
    """Return a random 6-digit string."""
    return str(random.randint(100000, 999999))


_EMAIL_CONFIGURED = (
    "@" in SMTP_SENDER_EMAIL
    and "your_gmail" not in SMTP_SENDER_EMAIL
    and len(SMTP_APP_PASSWORD.replace(" ", "")) == 16
)


def send_code(recipient_email: str, code: str) -> bool:
    """
    Send the 6-digit code via Gmail SMTP if credentials are configured.
    Falls back to printing the code in the terminal (demo mode) if not.
    Returns True on success, False on hard failure.
    """
    if not _EMAIL_CONFIGURED:
        # demo / no-setup mode: just show the code in the terminal
        print(f"\n[demo mode] email not configured.")
        print(f"  your login code is: {code}")
        print(f"  (in production this would be emailed to {recipient_email})\n")
        return True

    msg = MIMEText(f"Your login code is: {code}\n\nDo not share this with anyone.")
    msg["Subject"] = "Your login code"
    msg["From"] = SMTP_SENDER_EMAIL
    msg["To"] = recipient_email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SMTP_SENDER_EMAIL, SMTP_APP_PASSWORD)
            server.sendmail(SMTP_SENDER_EMAIL, recipient_email, msg.as_string())
        print(f"code sent to {recipient_email} — check your inbox.")
        return True
    except Exception as e:
        print(f"failed to send email: {e}")
        return False


def run_2fa(email: str) -> bool:
    """
    Generate a code, send/display it, then prompt the user to enter it.
    Returns True if correct code entered within 3 attempts, False otherwise.
    """
    code = generate_code()
    if not send_code(email, code):
        return False

    for attempt in range(3):
        entered = input("enter the 6-digit code: ").strip()
        if entered == code:
            return True
        remaining = 2 - attempt
        if remaining > 0:
            print(f"wrong code. {remaining} attempt(s) left.")

    print("too many wrong attempts. login denied.")
    return False
