""" Mail tasks """
from . import mail as util_mail
from steward_tasks import celery, StewardTask


@celery.task(base=StewardTask)
def mail(subject, body, mail_from=None, mail_to=None, host=None, port=None):
    """ Send mail via a celery task """
    util_mail(mail, subject, body, mail_from, mail_to, host, port)
