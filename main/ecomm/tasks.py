from celery.utils.log import get_task_logger
from django.core.mail import EmailMultiAlternatives
from django.template import loader
from django.utils import timezone
from main.celery import app
from main.settings import EMAIL_HOST_USER

from ecomm.models import Good, Subscriber

logger = get_task_logger(__name__)


@app.task
def send_confirmation_email(recipient_email, context):
    template = loader.get_template(template_name='ecomm/emails/signup_success.html')
    html_content = template.render(context=context)
    msg = EmailMultiAlternatives(
        subject='Confirm your email',
        body=html_content,
        from_email=EMAIL_HOST_USER,
        to=[recipient_email])
    msg.content_subtype = 'html'
    msg.send()


@app.task
def send_email_new_goods(goods_title):
    usernames_emails_list = list(Subscriber.objects.values('user__username', 'user__email'))
    for username_email in usernames_emails_list:
        template = loader.get_template(template_name='ecomm/emails/new_goods.html')
        html_content = template.render(context={'username': username_email['user__username'],
                                                'site_name': 'Ecomm', 'goods': goods_title})
        msg = EmailMultiAlternatives(
            subject='New goods',
            body=html_content,
            from_email=EMAIL_HOST_USER,
            to=[username_email['user__email']],
        )
        msg.content_subtype = 'html'
        msg.send()
        print('Email about new goods has been sent')


@app.task
def send_periodic_tasks():
    today = timezone.now()
    week_ago = today - timezone.timedelta(days=7)
    goods_title = [good.title for good in list(Good.objects.filter(pub_date__gte=week_ago))]
    send_email_new_goods.s(goods_title)
