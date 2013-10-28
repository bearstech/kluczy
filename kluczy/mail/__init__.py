from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
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

    def encrypt_sign_mime_message(self, target, message):
        m = MIMEMultipart('encrypted')
        m['protocol'] = 'application/pgp-encrypted'
        m.preamble = 'This is an OpenPGP/MIME encrypted message (RFC 2440 and 3156)'
        appli = MIMEApplication('Version: 1', 'pgp-encrypted',
                                encoders.encode_7or8bit)
        appli['Content-Description'] = 'PGP/MIME Versions Identification'
        m.attach(appli)
        plaintext = BytesIO(str(self.sign_mime_message(message)))
        ciphertext = BytesIO()
        self.ctx.armor = True
        recipient = self.ctx.get_key(target)
        self.ctx.encrypt_sign([recipient], gpgme.ENCRYPT_ALWAYS_TRUST,
                         plaintext, ciphertext)
        ciphertext.seek(0)
        appli_cipher = MIMEApplication(ciphertext.read(), 'octet-stream',
                                       encoders.encode_7or8bit)
        appli_cipher.add_header('Content-Disposition', 'inline',
                                filename='encrypted.asc')
        appli_cipher.add_header('Content-Type', 'application/octet-stream',
                                name='encrypted.asc')
        appli_cipher['Content-Description'] = 'OpenPGP encrypted message'
        m.attach(appli_cipher)
        return m


if __name__ == '__main__':
    from sendmail import SMTP
    import sys
    text = u"Hello world"
    part = MIMEText(text, 'plain')
    from_ = 'mlecarme@bearstech.com'
    to_ = sys.argv[1]
    context = Context(from_)
    signed = context.encrypt_sign_mime_message(to_, part)
    signed['From'] = from_
    signed['To'] = to_
    signed['Subject'] = 'GPG test with gpgme'
    signed['X-Pgp-Agent'] = 'kluczy 0.1'
    signed['Content-Description'] = 'OpenPGP encrypted message'
    signed['Content-Transfer-Encoding'] = '7bit'
    signed['X-Mailer'] = 'Python smtplib'
    with SMTP() as s:
        s.sendmail(from_, to_, signed.as_string())
