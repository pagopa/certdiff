import ssl
import socket
from cryptography import x509
from cryptography.hazmat._oid import ExtensionOID
from cryptography.hazmat.backends import default_backend

def fetch_certificate_from_url(url):
    hostname = url.replace("https://", "").replace("http://", "").split("/")[0]
    port = 443

    context = ssl.create_default_context()
    with socket.create_connection((hostname, port)) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            der_cert = ssock.getpeercert(binary_form=True)
            cert = x509.load_der_x509_certificate(der_cert, default_backend())
            return cert

def classify_certificates(certificate):
    try:
        is_ca = certificate.extensions.get_extension_for_oid(ExtensionOID.BASIC_CONSTRAINTS).value.ca
    except Exception as e:
        is_ca = False

    if certificate.issuer == certificate.subject and is_ca:
        return "root"
    elif is_ca:
        return "intermediate"
    else:
        return "leaf"

