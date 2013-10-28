from ConfigParser import SafeConfigParser
from os.path import expanduser
import smtplib

import keyring


"""
Put some configs in ~/.kluczy.cfg

[smtp]
host= mail.bearstech.com
port= 465
user= robert@bearstech.com

Add your secret password

$ python
>>> import keyring
>>> keyring.set_password('kluczy', 'smtp.password', 'toto')
"""


class SMTP(object):
    def __init__(self):
        self.conf = SafeConfigParser()
        self.conf.read([expanduser('~/.kluczy.cfg')])

    def __enter__(self):
        self.smtp = smtplib.SMTP_SSL(self.conf.get('smtp', 'host'),
                                     self.conf.get('smtp', 'port'))
        self.smtp.set_debuglevel(1)
        self.smtp.ehlo()
        user = self.conf.get('smtp', 'user')
        password = keyring.get_password('kluczy', 'smtp.password')
        self.smtp.login(user, password)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.smtp.quit()

if __name__ == "__main__":
    with SMTP() as s:
        print s
