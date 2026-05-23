# Security Policy

## Supported Versions

Security updates are applied on the default branch and included in active releases.

## Reporting a Vulnerability

Please report vulnerabilities privately to the maintainers instead of opening a public issue.

Include:
- vulnerability type
- affected file(s) and function(s)
- reproduction steps
- impact assessment
- suggested remediation (if available)

## Security baseline

- Never commit secrets or credentials
- Use environment variables for sensitive configuration
- Validate and sanitize external/user-provided input
- Keep dependencies updated
- Run baseline validation scripts before release:
  - `npm test`
  - `npm run build`
