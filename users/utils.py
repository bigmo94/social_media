from django.core.mail import send_mail


def send_verification_code(profile_email, verification_code):
    send_mail('Verification code', verification_code, 'yara company', [profile_email], fail_silently=False)
