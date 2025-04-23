import pytest
from certdiff.core import compare_certificates, load_certificate
from pathlib import Path
import json
from certdiff.utils import fetch_certificate_from_url

data_dir = Path(__file__).parent / "data"


@pytest.mark.parametrize("cert1_name, cert2_name, expect_diff", [
    ("ok_cert.pem", "ok_cert_clone.pem", False),
    ("ok_cert.pem", "bad_cert.pem", True),
])
def test_certificate_comparison(cert1_name, cert2_name, expect_diff, tmp_path):
    cert1 = load_certificate(data_dir / cert1_name)
    cert2 = load_certificate(data_dir / cert2_name)
    report_file = tmp_path / "report.json"

    diffs = compare_certificates(cert1, cert2, report_file=report_file)

    assert report_file.exists(), "Report JSON should be created"

    with open(report_file) as f:
        report_data = json.load(f)

    assert "old_certificate" in report_data
    assert "new_certificate" in report_data
    assert "differences" in report_data

    if expect_diff:
        assert diffs != [], "Expected differences, but none found"
        assert len(report_data["differences"]) > 0, "Expected differences in report"
    else:
        assert diffs == [], "Expected no differences, but found some"
        assert len(report_data["differences"]) == 0, "Expected no differences in report"


@pytest.mark.parametrize("cert1_name, cert2_name", [
    ("ok_cert.pem", "ok_cert_clone.pem"),
    ("ok_cert.pem", "bad_cert.pem"),
])
def test_json_report_contains_expected_fields(cert1_name, cert2_name, tmp_path):
    cert1 = load_certificate(data_dir / cert1_name)
    cert2 = load_certificate(data_dir / cert2_name)
    report_file = tmp_path / "report.json"

    compare_certificates(cert1, cert2, report_file=report_file)

    with open(report_file) as f:
        report_data = json.load(f)

    required_fields = ["old_certificate", "new_certificate", "differences"]
    for field in required_fields:
        assert field in report_data, f"Missing '{field}' in report"


@pytest.mark.parametrize("cert1_name, cert2_name, expect_diff", [
    ("test_leaf_ok.pem", "test_leaf_bad.pem", True),
])
def test_certificate_leaf_comparison(cert1_name, cert2_name, expect_diff, tmp_path):
    cert1 = load_certificate(data_dir / cert1_name)
    cert2 = load_certificate(data_dir / cert2_name)
    report_file = tmp_path / "report.json"

    diffs = compare_certificates(cert1, cert2, report_file=report_file)

    assert report_file.exists(), "Report JSON should be created"

    with open(report_file) as f:
        report_data = json.load(f)

    assert "old_certificate" in report_data
    assert "new_certificate" in report_data
    assert "differences" in report_data

    if expect_diff:
        assert diffs != [], "Expected differences, but none found"
        assert len(report_data["differences"]) > 0, "Expected differences in report"
    else:
        assert diffs == [], "Expected no differences, but found some"
        assert len(report_data["differences"]) == 0, "Expected no differences in report"


@pytest.mark.parametrize("cert1_name, cert2_name, expect_diff", [
    ("example.com", "ca.pem", True),
])
def test_certificate_from_uri_comparison(cert1_name, cert2_name, expect_diff, tmp_path):
    cert1 = [fetch_certificate_from_url(cert1_name)]
    cert2 = load_certificate(data_dir / cert2_name)
    report_file = tmp_path / "report.json"

    diffs = compare_certificates(cert1, cert2, report_file=report_file)

    assert report_file.exists(), "Report JSON should be created"

    with open(report_file) as f:
        report_data = json.load(f)

    assert "old_certificate" in report_data
    assert "new_certificate" in report_data
    assert "differences" in report_data

    if expect_diff:
        assert diffs != [], "Expected differences, but none found"
        assert len(report_data["differences"]) > 0, "Expected differences in report"
    else:
        assert diffs == [], "Expected no differences, but found some"
        assert len(report_data["differences"]) == 0, "Expected no differences in report"


@pytest.mark.parametrize("cert1_name, cert2_name, expect_diff", [
    ("cert_serial_1111.pem", "cert_serial_2222.pem", True),
])
def test_certificate_minor_changes(cert1_name, cert2_name, expect_diff, tmp_path):
    cert1 = load_certificate(data_dir / cert1_name)
    cert2 = load_certificate(data_dir / cert2_name)
    report_file = tmp_path / "report.json"

    diffs = compare_certificates(cert1, cert2, report_file=report_file)

    assert report_file.exists(), "Report JSON should be created"

    with open(report_file) as f:
        report_data = json.load(f)

    assert "old_certificate" in report_data
    assert "new_certificate" in report_data
    assert "differences" in report_data

    fields = {d['field'] for d in diffs}
    assert "subject" not in fields or "issuer" not in fields, \
        "Subject and Issuer is unattended here."

    if fields - {"subject", "issuer"}:
        assert diffs != [], "Expected differences, but none found"
        assert len(report_data["differences"]) > 0, "Expected differences in report"

@pytest.mark.parametrize("cert1_name, cert2_name, expect_diff", [
    ("test_leaf_ok.pem", "bad_cert.pem", True),
])
def test_certificate_leaf_comparison(cert1_name, cert2_name, expect_diff, tmp_path):
    cert1 = load_certificate(data_dir / cert1_name)
    cert2 = load_certificate(data_dir / cert2_name)
    report_file = tmp_path / "report.json"

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        diffs = compare_certificates(cert1, cert2, report_file=report_file)
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1
