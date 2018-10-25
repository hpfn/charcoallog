from celery.schedules import crontab
from celery.task import periodic_task
from celery.utils.log import get_task_logger
from django.utils import timezone

from charcoallog.bank.models import Extract, Schedule

LOGGER = get_task_logger(__name__)


@periodic_task(run_every=(crontab(hour=5, minute=0)), name='schedule')
def schedule():
    LOGGER.info('inicio de schedule')

    # this should go to other file
    date_now = timezone.now()
    date = date_now.strftime("%Y-%m-%d")

    until_today = Schedule.objects.filter(date__lte=date)
    for i in until_today.values():
        del i['id']
        Extract.objects.create(**i)
        Schedule.objects.filter(**i).delete()

    LOGGER.info('fim de schedule')
