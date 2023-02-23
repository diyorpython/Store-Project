from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string


def send_email_task(code, domain, email_template, subject, email):
    context_data = {
        "domain": domain,
        "protocol": "http",
        "code": code
    }
    message = render_to_string(email_template, context_data)
    send_mail(subject, message, settings.EMAIL_HOST_USER, [email], fail_silently=False)
    print("Message yuborildi")

def send_email_reset_password_task(domain, email_template, subject, email, uid, token):
    context_data = {
        "email": email,
        'domain': domain,
        "protocol": "http",
        "uid": uid,
        "Token": token
    }
    message = render_to_string(email_template, context_data)
    send_mail(subject, message, settings.EMAIL_HOST_USER, [email], fail_silently=False)
    print("message")