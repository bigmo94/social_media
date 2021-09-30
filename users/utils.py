from django.core.mail import send_mail

from users.models import Profile


def send_verification_code(profile_email, verification_code):
    send_mail(subject='Verification code', message=str(verification_code), from_email='yara company',
              recipient_list=[profile_email], fail_silently=False)


receivers = []
for profile in Profile.objects.all():
    receivers.append(profile.email)


def send_news_email():
    send_mail(subject='News', message='something', from_email='yara company', recipient_list=receivers,
              fail_silently=False)
