from kluczy import ssl
from OpenSSL import crypto
from os.path import exists
from os import unlink

KEY_EXTENSION = 'key'
CERTIFICATE_EXTENSION = 'crt'


class CertificateFactory(object):
    """
    Build certificate from a config file.
    """

    def __init__(self, conf):
        self.conf = conf
        self._cacert = None
        self._cakey = None

    @property
    def cakey(self):
        if self._cakey is None:
            key_name = 'CA.%s' % KEY_EXTENSION
            if exists(key_name):
                with open(key_name, 'rb') as kf:
                    cakey = crypto.load_privatekey(crypto.FILETYPE_PEM,
                                                   kf.read())
            else:
                cakey = self.createKeyPair('CA')
                # FIXME should drop every keys, nobody can live without its CA
            self._cakey = cakey
        return self._cakey

    @property
    def cacert(self):
        if self._cacert is None:
            ca_name = 'CA.%s' % CERTIFICATE_EXTENSION
            if exists(ca_name):
                with open(ca_name, 'rb') as caf:
                    cacert = crypto.load_certificate(crypto.FILETYPE_PEM,
                                                     caf.read())
            else:
                keys = dict([(key.upper(), value) for (key, value) in
                             self.conf.items('CA')])
                careq = self.createCertRequest(self.cakey, keys)
                ttl = self.conf.getint('SSL', 'ttl')
                digest = self.conf.get('SSL', 'digest')
                #FIXME Handle serial number
                #FIXME Handle version
                cacert = ssl.createCertificate(careq, (careq, self.cakey), 0,
                                               (0, ttl), digest)
                with open(ca_name, 'w') as certificate:
                    certificate.write(crypto.dump_certificate(
                        crypto.FILETYPE_PEM, cacert))
            self._cacert = cacert
        return self._cacert

    def createKeyPair(self, name):
        bits = self.conf.getint('SSL', 'key_size')
        key_path = "%s.%s" % (name, KEY_EXTENSION)
        if exists(key_path):
            return crypto.load_privatekey(crypto.FILETYPE_PEM,
                                          open(key_path, 'rb').read())
        cert_path = "%s.%s" % (name, CERTIFICATE_EXTENSION)
        if exists(cert_path):  # A certificate without a private key is useless
            unlink(cert_path)
        #FIXME does it works with DSA?
        pkey = ssl.createKeyPair(type=crypto.TYPE_RSA, bits=bits)
        open(key_path, 'w').write(crypto.dump_privatekey(crypto.FILETYPE_PEM,
                                                         pkey))
        return pkey

    def createCertRequest(self, pkey, keys):
        digest = self.conf.get('SSL', 'digest')
        return ssl.createCertRequest(pkey, digest=digest, **keys)

    def createCertificate(self, request, name):
        ttl = self.conf.getint('SSL', 'ttl')
        digest = self.conf.get('SSL', 'digest')
        cert_path = "%s.%s" % (name, CERTIFICATE_EXTENSION)
        if exists(cert_path):
            return crypto.load_certificate(crypto.FILETYPE_PEM,
                                           open(cert_path, 'rb').read())
        cert = ssl.createCertificate(request, (self.cacert, self.cakey), 1,
                                     (0, ttl), digest)
        open(cert_path, 'w').write(crypto.dump_certificate(crypto.FILETYPE_PEM,
                                                           cert))
        return cert

    def buildCertificates(self):
        template = self.conf.items('Certificate-keys')
        names = [name.strip() for name in
                 self.conf.get('Certificates', 'names').split(',')]
        for name in names:
            pkey = self.createKeyPair(name)
            #FIXME check string.format security
            keys = dict([(k.upper(), v.format(name=name))
                         for (k, v) in template if v is not ""])
            req = self.createCertRequest(pkey, keys)
            self.createCertificate(req, name)
