Kluczy
======

It should mean "key" in polish.

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

Licence
-------

Three terms BSD Licence, © Mathieu Lecarme.
