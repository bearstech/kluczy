from kluczy import ssl
from OpenSSL import crypto
from os.path import exists


class CertificateFactory(object):

    def __init__(self, conf):
        self.conf = conf
        self._cacert = None
        self._cakey = None

    @property
    def cakey(self):
        if self._cakey is None:
            if exists('CA.pkey'):
                cakey = crypto.load_privatekey(crypto.FILETYPE_PEM,
                                               open('CA.pkey', 'rb').read())
            else:
                cakey = self.createKeyPair(name='CA')
            self._cakey = cakey
        return self._cakey

    @property
    def cacert(self):
        if self._cacert is None:
            if exists('CA.cert'):
                cacert = crypto.load_certificate(crypto.FILETYPE_PEM,
                                                 open('CA.cert', 'rb').read())
            else:
                keys = dict([(key.upper(), value) for (key, value) in
                             self.conf.items('CA')])
                careq = self.createCertRequest(self.cakey, keys)
                ttl = self.conf.getint('SSL', 'ttl')
                digest = self.conf.get('SSL', 'digest')
                cacert = ssl.createCertificate(careq, (careq, self.cakey), 0,
                                               (0, ttl), digest)
                with open('CA.cert', 'w') as certificate:
                    certificate.write(crypto.dump_certificate(
                        crypto.FILETYPE_PEM, cacert))
            self._cacert = cacert
        return self._cacert

    def createKeyPair(self, name=None):
        bits = self.conf.getint('SSL', 'key_size')
        pkey = ssl.createKeyPair(bits=bits)
        if name is not None:
            with open('%s.pkey' % name, 'w') as private_key:
                private_key.write(crypto.dump_privatekey(crypto.FILETYPE_PEM,
                                                         pkey))
        return pkey

    def createCertRequest(self, pkey, keys):
        digest = self.conf.get('SSL', 'digest')
        return ssl.createCertRequest(pkey, digest=digest, **keys)

    def createCertificate(self, request, name=None):
        ttl = self.conf.getint('SSL', 'ttl')
        digest = self.conf.get('SSL', 'digest')
        cert = ssl.createCertificate(request, (self.cacert, self.cakey), 1,
                                     (0, ttl), digest)
        if name is not None:
            with open('%s.cert' % name, 'w') as certificate:
                certificate.write(crypto.dump_certificate(
                    crypto.FILETYPE_PEM, cert))
        return cert

    def buildCertificates(self):
        template = self.conf.items('Certificate-keys')
        names = [name.strip() for name in
                 self.conf.get('Certificates', 'names').split(',')]
        for name in names:
            pkey = self.createKeyPair(name)
            #FIXME check string.format security
            keys = dict([(k.upper(), v.format(name=name))
                         for (k, v) in template
            ])
            req = self.createCertRequest(pkey, keys)
            self.createCertificate(req, name)
