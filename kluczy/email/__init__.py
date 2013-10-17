from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email import encoders

import getpass
import os
try:
    from io import BytesIO
except ImportError:
    from StringIO import StringIO as BytesIO

import gpgme


class Context(object):
    def __init__(self, user):
        self.ctx = gpgme.Context()
        self.ctx.armor = True
        signer = self.ctx.get_key(user)
        assert signer.can_sign
        assert signer.can_encrypt
        self.ctx.signers = [signer]
        self.password = getpass.getpass("Pass phrase : ")
        self.ctx.passphrase_cb = self.passphrase_cb

    def passphrase_cb(self, uid_hint, passphrase_info, prev_was_bad, fd):
        os.write(fd, self.password + b'\n')

    def sign_mime_message(self, message):
        m = MIMEMultipart('signed')
        m['protocol'] = 'application/pgp-signature'
        m.attach(message)
        plaintext = BytesIO(str(message))
        signature = BytesIO()

        self.ctx.sign(plaintext, signature, gpgme.SIG_MODE_NORMAL)
        signature.seek(0)
        mime_app_sign = MIMEApplication(signature.read(), 'pgp-signature',
                                        encoders.encode_7or8bit)
        mime_app_sign['Content-Description'] = 'Message signed with gpg using pygpgme'
        mime_app_sign.add_header('Content-Disposition',  'attachment',
                                 filename='signature.asc')
        mime_app_sign.add_header('Content-Type', 'application/pgp-signature',
                                 name='signature.asc')


        m.attach(mime_app_sign)
        return m


if __name__ == '__main__':
    from email.mime.text import MIMEText
    text = u"Hello world"
    part = MIMEText(text, 'plain')
    context = Context('mlecarme@bearstech.com')
    signed = context.sign_mime_message(part)
    print signed
