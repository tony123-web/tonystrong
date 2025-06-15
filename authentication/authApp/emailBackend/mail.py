import ssl
from django.core.mail.backends.smtp import EmailBackend as SMTPBackend
from django.utils.functional import cached_property

class MyEmailBackend(SMTPBackend):
    @cached_property
    def ssl_context(self):
        if self.ssl_certfile or self.ssl_keyfile:
            ssl_contex=ssl.SSLContext(protocol=ssl.PROTOCOL_TLS_CLIENT)
            ssl_contex.load_cert_chain(self.ssl_certfile, self.ssl_keyfile)
            return ssl_contex
        else:
            ssl_contex=ssl.create_default_context()
            ssl_contex.check_hostname=False
            ssl_contex.verify_mode=ssl.CERT_NONE
            return ssl_contex