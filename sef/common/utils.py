from django.core.mail import EmailMultiAlternatives

def send_email_async(from_email, recipients, subject, body, html_message='',
                     attachments=None, bcc=None, cc=None):

    alternatives = None
    if html_message:
        alternatives = [(html_message, 'text/html')]
    mail = EmailMultiAlternatives(
        subject=subject, body=body, from_email=from_email, to=recipients,
        bcc=bcc, cc=cc, attachments=attachments, alternatives=alternatives
    )
    return mail.send()
