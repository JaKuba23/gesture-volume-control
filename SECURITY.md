## Security Policy

### Supported Versions

Currently supported versions with security updates:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

### Reporting a Vulnerability

We take security vulnerabilities seriously. If you discover a security issue, please follow responsible disclosure practices.

#### How to Report

**DO NOT** open a public GitHub issue for security vulnerabilities.

Instead, please report security issues privately via GitHub Security Advisories:
**Security tab → Report a vulnerability**

#### What to Include

Your report should include:

1. **Description** of the vulnerability
2. **Steps to reproduce** the issue
3. **Potential impact** of the vulnerability
4. **Affected versions**
5. **Suggested fix** (if you have one)
6. **Your contact information** for follow-up

#### Response Timeline

- **Initial response:** Within 48 hours
- **Status update:** Within 7 days
- **Fix timeline:** Depends on severity
  - Critical: 1-7 days
  - High: 7-14 days
  - Medium: 14-30 days
  - Low: 30-90 days

### Security Best Practices

When using Motus:

1. **Camera Permissions:**
   - Grant camera access only to trusted applications
   - Revoke permissions when not needed
   - Review macOS Privacy settings regularly

2. **Dependencies:**
   - Keep dependencies updated
   - Review dependency security advisories
   - Use `safety check` to scan for known vulnerabilities

3. **Execution:**
   - Run from trusted sources only
   - Review code before executing
   - Use virtual environments

4. **Network:**
   - Motus does not make network connections
   - Camera data is processed locally only
   - No data is transmitted externally

### Known Security Considerations

#### Camera Access

Motus requires camera access to function. This is:
- **Local only:** All processing happens on your machine
- **No recording:** No video is saved to disk
- **No transmission:** No data leaves your device

#### Volume Control

Motus controls system volume via AppleScript:
- **macOS only:** Uses osascript command
- **User-level permissions:** No elevated privileges required
- **Isolated:** Cannot access other system settings

### Security Scanning

This project uses automated security scanning:

- **Bandit:** Python code security analysis
- **Safety:** Dependency vulnerability checking
- **Trivy:** Container image scanning
- **Dependabot:** Automated dependency updates

### Development Security

Contributors must:

1. Never commit secrets or credentials
2. Use environment variables for configuration
3. Follow secure coding practices
4. Run security scans before submitting PRs
5. Review dependencies for security issues

### Disclosure Policy

Once a security issue is fixed:

1. A security advisory will be published
2. Affected users will be notified
3. Fix will be included in next release
4. Credit given to reporter (if desired)

### Contact

For security concerns, contact:

- **Maintainer:** @JaKuba23
- **Report privately via:** GitHub Security Advisories (Security tab → Report a vulnerability)

---

Thank you for helping keep Motus secure.

