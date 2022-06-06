from apps.users.models import User
from django.core.mail import EmailMessage
import random
from django.conf import settings
import threading


class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()
        print('SENT EMAIL')

def send_otp_via_email(email):
    subject = 'Your account verification email'
    otp = random.randint(100000, 999999)
    message = f"Your otp is {otp}"
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    mail = EmailMessage(subject, message, email_from,
                                     recipient_list)
    # mail.send()  
    EmailThread(mail).start()                             
    user_obj = User.objects.get(email = email)
    user_obj.otp = otp
    user_obj.save()


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