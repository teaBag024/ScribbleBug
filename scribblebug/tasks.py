from celery import shared_task
from .scribble_utils import create_scribble

@shared_task
def create_scribble_task(user, keywords):
    scribble = create_scribble(user, keywords)
    return scribble.id