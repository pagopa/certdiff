import json
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from rich.console import Console

console = Console()


def load_certificate(cert_path):
    with open(cert_path, 'rb') as f:
        cert_data = f.read()
        return x509.load_pem_x509_certificate(cert_data, default_backend())


def extract_certificate_info(cert):
    return {
        "subject": cert.subject.rfc4514_string(),
        "issuer": cert.issuer.rfc4514_string(),
        "serial_number": hex(cert.serial_number),
        "not_valid_before": cert.not_valid_before_utc.isoformat(),
        "not_valid_after": cert.not_valid_after_utc.isoformat(),
        "fingerprint_sha256": cert.fingerprint(hashes.SHA256()).hex()
    }


def compare_certificates(old_cert_input, new_cert_input, verbose=False, report_file=None):
    differences = []

    if isinstance(old_cert_input, (str, bytes)):
        old_cert = load_certificate(old_cert_input)
    else:
        old_cert = old_cert_input

    if isinstance(new_cert_input, (str, bytes)):
        new_cert = load_certificate(new_cert_input)
    else:
        new_cert = new_cert_input

    old_info = extract_certificate_info(old_cert)
    new_info = extract_certificate_info(new_cert)

    if verbose:
        console.print("[bold cyan]🔍 Verbose mode enabled.[/bold cyan]")
        console.print("[blue]Old certificate info:[/blue]")
        for key, value in old_info.items():
            console.print(f"  {key}: {value}")

        console.print("[magenta]New certificate info:[/magenta]")
        for key, value in new_info.items():
            console.print(f"  {key}: {value}")

    fields_to_compare = ["subject", "issuer"]

    for field in fields_to_compare:
        if old_info[field] != new_info[field]:
            differences.append({
                "field": field,
                "old": old_info[field],
                "new": new_info[field]
            })

    if report_file:
        report_data = {
            "old_certificate": old_info,
            "new_certificate": new_info,
            "differences": differences
        }
        with open(report_file, 'w') as f:
            json.dump(report_data, f, indent=4)
        console.print(f"[bold cyan]📝 Report saved to:[/bold cyan] {report_file}")

    return differences
