import sys
import os
import getpass
try:
    from io import BytesIO
except ImportError:
    from StringIO import StringIO as BytesIO

import gpgme


ctx = gpgme.Context()

#for key in ctx.keylist():
    #for sk in key.subkeys:
        #print sk.pubkey_algo, sk.keyid, sk.fpr
    #for uid in key.uids:
        #print uid.name, uid.email

plaintext = BytesIO(b'Hello World\n')
ciphertext = BytesIO()
ctx.armor = True
signer = ctx.get_key('mlecarme@bearstech.com')
assert signer.can_encrypt
assert signer.can_sign
target = sys.argv[1]
recipient = ctx.get_key(sys.argv[1])
ctx.signers = [signer]


def passphrase_cb(uid_hint, passphrase_info, prev_was_bad, fd):
    password = getpass.getpass("Pass phrase for %s : " % uid_hint)
    os.write(fd, password + b'\n')

ctx.passphrase_cb = passphrase_cb
try:
    new_sigs = ctx.encrypt_sign([recipient], gpgme.ENCRYPT_ALWAYS_TRUST,
                                plaintext, ciphertext)
except gpgme.GpgmeError as exc:
    print exc
    assert exc.args[0] == gpgme.ERR_SOURCE_GPGME
    assert exc.args[1] == gpgme.ERR_BAD_PASSPHRASE
ciphertext.seek(0)
print ciphertext.read()
