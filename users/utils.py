from django.core.mail import send_mail


def send_verification_code(profile_email, verification_code):
    send_mail(subject='Verification code', message=str(verification_code), from_email='yara company',
              recipient_list=[profile_email], fail_silently=False)
