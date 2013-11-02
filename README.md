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

### Secure server with an unauthenticated client

First, a server :

    openssl s_server -cert alice.cert -key alice.pkey

Then, a client :

    openssl s_client -connect localhost:4433 -CAfile CA.cert

Both output are verbose, enjoy. What you write client side display server side.

Licence
-------

Three terms BSD Licence, © Mathieu Lecarme.
