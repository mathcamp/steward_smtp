""" Steward extension for sending mail via SMTP """
import json
import smtplib
from email.mime.text import MIMEText

from pyramid.httpexceptions import HTTPBadRequest
from pyramid.view import view_config


NO_ARG = object()


def _get_arg_with_default(request, arg, setting, default=NO_ARG):
    """
    Convenience method for getting a request parameter and falling back to a
    setting in the config file if it is not present.

    Parameters
    ----------
    arg : str
        The name of the arg
    setting : str
        The name of the setting to use as the default
    default : object, optional
        The default value to fall back to if not present in settings

    """
    value = request.param(arg, None)
    if value is None:
        value = request.registry.settings.get(setting)
    if value is None:
        if default is NO_ARG:
            raise HTTPBadRequest("Missing argument '{}' and '{}' not found in "
                                 "config file!".format(arg, setting))
        else:
            return default
    return value


def mail(config, subject, body, mail_from=None, mail_to=None, host=None, port=None):
    if mail_from is None:
        mail_from = config['smtp.from']
    if mail_to is None:
        mail_to = config['smtp.to']
    if host is None:
        host = config.get('smtp.server', 'localhost')
    if port is None:
        port = int(config.get('smtp.port', 25))
    try:
        mail_to_list = json.loads(mail_to)
        mail_to = ', '.join(mail_to_list)
    except:
        mail_to_list = [addr.strip() for addr in mail_to.split(',')]

    email = MIMEText(body)
    email['Subject'] = subject
    email['From'] = mail_from
    email['To'] = mail_to
    s = smtplib.SMTP(host, port)
    s.sendmail(mail_from, mail_to_list, email.as_string())
    s.quit()


@view_config(route_name='mail', request_method='POST', permission='mail')
def send_mail(request):
    """
    Send an email

    Parameters
    ----------
    subject : str
        The subject of the email
    body : str
        The body of the email
    mail_from : str, optional
        The address to mail from (defaults to value in conf file)
    mail_to : str or list, optional
        The address(es) to mail to (defaults to value in conf file). Should be
        a comma-delimited string or a list.
    smtp_server : str, optional
        The SMTP server to mail from (defaults to value in conf file or
        'localhost')
    smtp_port : int, optional
        The port to use on the SMTP server (defaults to value in conf file or
        25)

    """
    mail(request.registry.settings,
         request.param('subject'), request.param('body'),
         request.param('mail_from', None), request.param('mail_to', None),
         request.param('host', None), request.param('port', None))
    return request.response


def mail(client, subject, body, smtp_to=None, smtp_from=None, smtp_server=None,
         smtp_port=None):
    """

    Send an email via SMTP

    Parameters
    ----------
    subject : str
        The subject of the email
    body : str
        The body for the email
    smtp_to : str, optional
        The 'to' address(es) (comma-delimited) (default specified in ini file)
    smtp_from : str, optional
        The 'from' address (default specified in ini file)
    smtp_server : str, optional
        The hostname of the SMTP server (default specified in ini file)
    smtp_port : int, optional
        The port the SMTP server is running on (default specified in ini file)

    """
    kwargs = {
        'subject': subject,
        'body': body,
    }
    if smtp_to is not None:
        kwargs['mail_to'] = smtp_to
    if smtp_from is not None:
        kwargs['mail_from'] = smtp_from
    if smtp_server is not None:
        kwargs['smtp_server'] = smtp_server
    if smtp_port is not None:
        kwargs['smtp_port'] = smtp_port
    client.cmd('mail', **kwargs)


def include_client(client):
    """ Add mail command to client """
    client.set_cmd('mail', mail)


def includeme(config):
    """ Configure the app """
    config.add_acl_from_settings('smtp')
    config.add_route('mail', '/mail')
    config.scan()
