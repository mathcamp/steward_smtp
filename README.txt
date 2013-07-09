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
* **smtp.from** - The default 'from' address (optional)
* **smtp.to** - The default 'to' addresses (comma-separated, optional)
* **smtp.server** - The SMTP server (optional, default 'localhost')
* **smtp.port** - The SMTP port (optional, default 25)

Permissions
===========
* **mail.perm.mail** - This permission is required to send mail
