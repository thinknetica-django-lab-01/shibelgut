import logging
from apscheduler.schedulers.blocking import BlockingScheduler
from django.core.management import BaseCommand
from ecomm.sending_email import send_email_by_scheduler
from django.conf import settings

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_job(send_email_by_scheduler, 'interval', days=7, id='send_email_by_scheduler',
                          replace_existing=True)
        logger.info('Sent email')
        try:
            logger.info('Starting scheduler...')
            print('Starting scheduler...')
            scheduler.start()
        except KeyboardInterrupt:
            logger.info('Stopping scheduler...')
            print('Stopping scheduler...')
            scheduler.shutdown()
            logger.info('Scheduler shut down successfully.')
            print('Scheduler shut down successfully.')
