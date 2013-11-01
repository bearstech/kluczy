from setuptools import setup

setup(
    name='kluczy',
    version=0.1,
    description='Handling RSA keys, both ssl and gpg',
    license='BSD',
    author='Mathieu Lecarme',
    author_email='mlecarme@bearstech.com',
    keywords=['rsa', 'certificate', 'gpg', 'ssl'],
    url='https://github.com/bearstech/kluczy',
    install_requires=['pygpgme', 'keyring', 'pyOpenSSL'],
    packages=['kluczy'],
    scripts=['scripts/kluczy'],
    classifiers=[],
)
