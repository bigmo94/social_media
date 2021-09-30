from celery import shared_task
from celery.utils.log import get_task_logger

from .utils import send_verification_code, send_news_email

logger = get_task_logger(__name__)


@shared_task
def send_verification_code_task(profile_email, verification_code):
    logger.info("Sent email")
    send_verification_code(profile_email, verification_code)


@shared_task(name='send_news')
def send_news_email_task():
    logger.info("sent_news")
    send_news_email()


