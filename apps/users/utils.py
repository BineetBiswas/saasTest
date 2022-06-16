from apps.users.models import User
from django.core.mail import EmailMessage
import random
from django.conf import settings
from django.core.cache import cache
import threading
import pyotp



class generateKey:
    @staticmethod
    def returnValue():
        secret = pyotp.random_base32()        
        totp = pyotp.TOTP(secret, interval=120)
        OTP = totp.now()
        return {"totp":secret,"OTP":OTP}


class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()
        print('SENT EMAIL')

# def send_otp_via_email(email):
#     subject = 'Your account verification email'
#     otp = random.randint(100000, 999999)
#     message = f"Your otp is {otp}"
#     email_from = settings.EMAIL_HOST_USER
#     recipient_list = [email]
#     mail = EmailMessage(subject, message, email_from,
#                                      recipient_list)
#     # mail.send()  
#     EmailThread(mail).start()                             
#     user_obj = User.objects.get(email = email)
#     user_obj.otp = otp
#     user_obj.save()


# def send_login_otp_via_email(email):
#     subject = 'Your account verification email'
#     otp = random.randint(100000, 999999)
#     message = f"Your login otp is {otp}"
#     email_from = settings.EMAIL_HOST_USER
#     recipient_list = [email]
#     mail = EmailMessage(subject, message, email_from,
#                                      recipient_list)
#     # mail.send()  
#     EmailThread(mail).start()                             
#     user_obj = User.objects.get(email = email)
#     user_obj.otp = otp
#     user_obj.save()


def send_otp_via_email(email):
    if cache.get(email):
        return False, cache.ttl(email)
    subject = 'Your account verification email'
    key = generateKey.returnValue()
    otp = key['OTP']
    activation_key = key['totp']
    message = f"Your otp is {otp}"
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    mail = EmailMessage(subject, message, email_from,
                                     recipient_list)
    # mail.send()  
    EmailThread(mail).start()                             
    user_obj = User.objects.get(email = email)
    user_obj.otp = otp
    user_obj.activation_key = activation_key
    user_obj.set_password(activation_key)
    # cache.set("foo", "value", timeout= 120)
    cache.set(email, otp, timeout= 120)
    user_obj.save()
    return True, 0