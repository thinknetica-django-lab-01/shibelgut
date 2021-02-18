from django.core.mail import EmailMultiAlternatives
from django.template import loader
from main.settings import EMAIL_HOST_USER
from ecomm.models import Subscriber


def send_email_by_scheduler():
    usernames_emails_list = list(Subscriber.objects.values('user__username', 'user__email'))
    for username_email in usernames_emails_list:
        template = loader.get_template(template_name='ecomm/emails/new_goods.html')
        html_content = template.render(context={'username': username_email['user__username'], 'site_name': 'Ecomm'})
        msg = EmailMultiAlternatives(
            subject='New goods',
            body=html_content,
            from_email=EMAIL_HOST_USER,
            to=[username_email['user__email']],
        )
        msg.content_subtype = 'html'
        msg.send()
