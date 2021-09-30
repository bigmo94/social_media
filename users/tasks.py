from celery import shared_task
from celery.utils.log import get_task_logger

from .utils import send_verification_code

logger = get_task_logger(__name__)


@shared_task
def send_verification_code_task(profile_email, verification_code):
    logger.info("Sent email")
    return send_verification_code(profile_email, verification_code)
