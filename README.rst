Steward SMTP
============
This is a Steward extension for sending email via SMTP.

Setup
=====
To use steward_smtp, just add it to your includes either programmatically::

    config.include('steward_smtp')

or in the config.ini file::

    pyramid.includes = steward_smtp

Make sure you include it in the client config file as well.

Configuration
=============
::

    # The default 'from' address (optional)
    smtp.from = bot@company.com

    # The default 'to' addresses (comma-separated, optional)
    smtp.to = alerts@company.com,sysadmin@company.com

    # The SMTP server (optional, default 'localhost')
    smtp.server = smtp.company.com

    # The SMTP port (optional, default 25)
    smtp.port = 25

Permissions
===========
::

    # This permission is required to send mail
    mail.perm.mail = group1 group2
