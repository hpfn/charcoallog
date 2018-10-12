from celery.schedules import crontab
from celery.task import periodic_task
from celery.utils.log import get_task_logger
from django.utils import timezone

from charcoallog.bank.models import Extract, Schedule

logger = get_task_logger(__name__)


@periodic_task(run_every=(crontab(hour=5, minute=0)), name='schedule')
def schedule():
    logger.info('inicio de schedule')

    # this should go to other file
    date_now = timezone.now()
    date = date_now.strftime("%Y-%m-%d")

    until_today = Schedule.objects.filter(date__lte=date)
    for i in until_today.values('user_name', 'date', 'money', 'description', 'category', 'payment'):
        Extract.objects.create(**i)
        Schedule.objects.filter(**i).delete()

    logger.info('fim de schedule')
