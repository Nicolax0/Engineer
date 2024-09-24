import smtplib
import os
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import dns.resolver

def is_valid_id(email):
    has_dns = False
    # verify using dns/mx records
    try:
        result = dns.resolver.resolve(email, 'MX')
        has_dns = True # rcs email was or is a student
    except:
        return 0 # rcs email was never a student
    
    # verify using smtp
    domain = email.split('@')[1]
    try:
        server = smtplib.SMTP('smtp.' + domain)
        server.set_debuglevel(0)
        server.ehlo()
        server.mail('')
        code, message = server.rcpt(email)
        server.quit()

        if code == 250:
            return 2 # is a current student
        return 1 # was a student but not anymore

    except Exception as e:
        print(f"Error: {e}")
        return 3 # there was an error
    
def generate_random_code():
    random.randint(100000, 999999)

def send_verification_code(RCSID, discord_id):
    email = RCSID + "@rpi.edu"
    status = is_valid_id(email)

    if status == 0:
        return 0
    elif status == 1:
        return 1
    elif status == 2:
        # message = MIMEMultipart()
        # message['From'] = os.getenv("GMAIL")
        # message['To'] = email
        # message["Subject"] = "Verification Code"

        # #message.attach(MIMEText(body, "plain"))
        # try:
        #     server = smtplib.SMTP('smtp.gmail.com', 587)
        #     server.starttls()
        #     server.login(os.getenv("GMAIL"), os.getenv("GMAIL_PASS"))
        #     server.sendmail(os.getenv("GMAIL"), email, message.as_string())
        #     server.quit()
        # except:
        #     return 4 # is a current student but failed to send email
        return 2 # is a current student and email was sent
    elif status == 3:
        return 3
    return 5 # unknown error
    

    
