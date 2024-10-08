import smtplib
import os
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import dns.resolver

    
def generate_random_code():
    random.randint(100000, 999999)


# add functionality to check if RCSID is already in database
def send_verification_code(RCSID, discord_id):
    email = RCSID + "@rpi.edu"    
    message = MIMEMultipart()
    message['From'] = os.getenv("GMAIL")
    message['To'] = email
    message["Subject"] = "Verification Code"

    message.attach(MIMEText("this is a test email", "plain"))
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(os.getenv("GMAIL"), os.getenv("GMAIL_PASS"))
        server.sendmail(os.getenv("GMAIL"), email, message.as_string())

        print(f"Email successfully sent to {email}")
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False
    finally:
        try:
            server.quit()
        except Exception as quit_error:
            print(f"Failed to close the connection properly: {quit_error}")
    return True
    

    
