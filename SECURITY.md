# Security Policy

## Reporting a Vulnerability
Please report vulnerabilities privately to the repository maintainers. Include:
- Impact summary
- Reproduction steps
- Affected files/endpoints
- Suggested remediation (if known)

## Security Baseline
- Keep secrets in environment variables; never commit secrets.
- Validate and sanitize external/user input.
- Use least-privilege permissions for deployed services.
- Keep dependencies updated and review advisories regularly.

## Current Security-Sensitive Areas
- Browser automation credential handling
- API endpoints and CORS configuration
- Docker/runtime environment variable management
