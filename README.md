# 🔍 CertDiff 🔒

![Python](https://img.shields.io/badge/python-3.12+-blue?logo=python)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-active-brightgreen)

**CertDiff** is a smart utility designed to compare two X.509 certificates and detect critical differences.

It’s perfect for automation pipelines to prevent unexpected changes during certificate renewals — like Issuer changes, CN changes.

---

## ✨ Features

- ✅ **Certificate field comparison**:
  - Subject
  - Issuer
- ✅ **Verbose human-readable output**
- ✅ **JSON report generation**
- ✅ **Exit codes** suitable for pipeline automation:
  - `0` → No differences
  - `1` → Differences detected

---

## 🚀 Installation

1. Make sure you have [PDM](https://pdm.fming.dev/latest/#installation) installed:

```bash
python -m pip install pdm
```

2. Install dependencies
```bash
pdm install
```

## 🔥 Usage

Basic command:

```bash
pdm run certdiff --old ./path/to/old_cert.pem --new ./path/to/new_cert.pem
```

With verbose output:

```bash
pdm run certdiff --old ./path/to/old_cert.pem --new ./path/to/new_cert.pem --verbose
```

Generate JSON report:

```bash
pdm run certdiff --old ./path/to/old_cert.pem --new ./path/to/new_cert.pem --report-json ./report.json
```

## 📂 Output

✅ Console Output: Summary of differences or confirmation that certificates are equivalent.

📝 Optional JSON Report: Full details of both certificates and a list of differences.

🔖 Exit codes: For CI/CD automation.

Example of console output:

    ✅ Certificates are equivalent.

Or:

    ❌ Certificates differ:
    - Subject: CN=test.example.com ➔ CN=different.example.com
    - Serial Number: 0x14a3d... ➔ 0x58bf3...

Example of JSON report:

    {
      "old_certificate": {
        "subject": "CN=test.example.com,O=TestOrg,L=Test,ST=Test,C=IT",
        "issuer": "CN=Test Root CA,O=Test,L=Test,ST=Test,C=IT",
        ...
      },
      "new_certificate": {
        "subject": "CN=different.example.com,O=TestOrg,L=Test,ST=Test,C=IT",
        "issuer": "CN=Test Root CA,O=Test,L=Test,ST=Test,C=IT",
        ...
      },
      "differences": [
        {
          "field": "subject",
          "old": "CN=test.example.com,O=TestOrg,L=Test,ST=Test,C=IT",
          "new": "CN=different.example.com,O=TestOrg,L=Test,ST=Test,C=IT"
        },
        ...
      ]
    }

