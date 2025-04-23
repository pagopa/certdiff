import os.path

import click
from .core import compare_certificates, load_certificate
from .utils import fetch_certificate_from_url


@click.command()
@click.option('--old', 'old_cert_path', type=click.Path(exists=True),
              help='Path to the old certificate PEM file.')
@click.option('--old-url', 'old_cert_url',
              help='URL to fetch the old certificate from a remote HTTPS endpoint.')
@click.option('--new', 'new_cert_path', required=True, type=click.Path(exists=True),
              help='Path to the new certificate PEM file.')
@click.option('--verbose', is_flag=True, help='Enable verbose output.')
@click.option('--report-json', 'report_file', default=None,
              help='Optional: Output a JSON report of the comparison.')
def main(old_cert_path, old_cert_url, new_cert_path, verbose, report_file):
    """
    CertDiff 🛡️
    Compare two certificates and report differences.
    """

    if not old_cert_path and not old_cert_url:
        raise click.ClickException("You must specify either --old or --old-url.")

    if old_cert_path:
        old_cert = load_certificate(old_cert_path)
    else:
        old_cert = [fetch_certificate_from_url(old_cert_url)]

    new_cert = load_certificate(new_cert_path)

    differences = compare_certificates(old_cert, new_cert, verbose, report_file)

    if differences:
        click.secho("❌ Certificates differ:", fg='red')
        for diff in differences:
            click.echo(f"- [{diff['type']}] {diff['field'].title()}: {diff['old']} ➔ {diff['new']}")
        raise SystemExit(1)
    else:
        click.secho("✅ Certificates are equivalent.", fg='green')
        raise SystemExit(0)


if __name__ == '__main__':
    main()
