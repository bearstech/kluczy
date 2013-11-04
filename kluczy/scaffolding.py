import os.path
import uuid
import glob
import os

DEFAULT="""
[Main]
id=%s
[SSL]
key_size=2048
digest=sha256
#Three years
ttl=94608000

[CA]
#Common Name
CN=Certificate Authority
#Country
C=FR
#State
#ST=
#Locality
L=Paris
#Organisation
O=
#Organisation Unit
OU=

[Certificates]
names=alice, bob, celia

[Certificate-keys]
CN={name}.kluczy.org
C=FR
L=Paris
O=Kluczy
"""

def main():
    if not os.path.exists('config.ini'):
        with open('config.ini', 'w') as f:
            f.write(DEFAULT % uuid.uuid1())
        for rotten in glob.glob('*.crt') + glob.glob('*.key'):
            os.unlink(rotten)
