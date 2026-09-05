"""SSL context used for every connection to ARCA (ex AFIP) web services.

ARCA's production servers still negotiate TLS with 1024-bit Diffie-Hellman
parameters. Debian ships OpenSSL with security level 2 compiled in as the
default, and level 2 rejects DH keys below 2048 bits, so any request to
production fails during the TLS handshake with:

    [SSL: DH_KEY_TOO_SMALL] dh key too small

Note that this is NOT set in /etc/ssl/openssl.cnf on the python:3.11-slim
image (the file has no SECLEVEL line at all) - it is the library default,
which is why it has to be overridden here in code rather than by patching a
config file. Homologation servers are not affected, so this only shows up the
first time the service is pointed at production.

Lowering the level to 1 restores support for those DH parameters. Server
certificate verification and hostname checking are left untouched: what is
relaxed is only which key exchange parameters are considered acceptable.
"""

import ssl


def build_arca_ssl_context() -> ssl.SSLContext:
    context = ssl.create_default_context()
    context.set_ciphers("DEFAULT@SECLEVEL=1")
    return context
