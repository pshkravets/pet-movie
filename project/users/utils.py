from django.core.mail import send_mail


def send_otp_email(email, otp):
    send_mail(
        'Hello from project!',
        f'Hi there dear user! Your password is {otp}',
        'settings.EMAIL_HOST_USER',
        [email],
        fail_silently=False
    )