Kluczy
======

It means "key" in polish.

Install
-------

### Debian and Ubuntu

    apt-get install python-gpgme python-keyring python-openssl

### OSX

    brew install gpgme

Install your own virtualenv and requirements.

    env ARCHFLAGS="-arch x86_64" pip install -r requirements.txt

You can read SSL certificate with QuickLook.

Try it
------

    kluczy init

Read the comments and edit the config.ini file

    kluczy run

A Certificate Authority is lazily created


Testing certificates
--------------------

Openssl provides tools for testing and debugging SSL.
Generate some certificates with the default config.ini

### Watch what you done

Alice private key :

    openssl rsa -in alice.key -check

Alice certificate :

    openssl x509 -in alice.crt -text

### Secure server with an unauthenticated client

First, a server :

    openssl s_server -cert alice.crt -key alice.key

Then, a client :

    openssl s_client -connect localhost:4433 -CAfile CA.crt

Both output are verbose, enjoy. What you write client side display server side.

### Secure server with authenticated client

Alice got a server, and verify clients :

    openssl s_server -cert alice.crt -key alice.key -CAfile CA.crt -Verify 1

Bob can connect it, they use the same Certificate Authority :

    openssl s_client -connect localhost:4433 -CAfile CA.crt -cert bob.crt -key bob.key

Features
--------

 * √ Declarative certificates generation
 * √ Sending mail with MIME and GPG
 * √ Authenticated SMTP using the keyring
 * _ Cascading certificate authority and chaining them
 * _ Revocation list
 * _ Pin code for private keys
 * _ Batch sending certificates with GPG mail
 * _ Handling DH param
 * _ RSA, DSA or ECDSA private key
 * _ PEM or DER output format

Licence
-------

Three terms BSD Licence, © Mathieu Lecarme.
