import pytest
from certdiff.core import load_certificate
from pathlib import Path

data_dir = Path(__file__).parent / "data"

@pytest.mark.parametrize("cert1_name, is_cert", [
    ("ca.pem", True),
])
def test_load_certificates(cert1_name, is_cert, tmp_path):
    cert1 = load_certificate(data_dir / cert1_name)

    if is_cert:
        assert cert1 is not None, f"'{cert1_name}' exists and is a certificate."
