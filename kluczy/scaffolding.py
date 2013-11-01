import os.path

DEFAULT="""
[SSL]
key_size=2048
digest=sha256
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

[Clients]
"""

def main():
    if not os.path.exists('config.ini'):
        with open('config.ini', 'w') as f:
            f.write(DEFAULT)
