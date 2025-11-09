# Lab 4.1  HTTP Basics: Requests, HTML Parsing & Response Analysis

## Which server headers you observed — were they helpful?

These are the server headers i observed:

- **scanme.nmap.org**: `Apache/2.4.7 (Ubuntu)` - Very specific, reveals exact software versions
- **example.com**: No server header - Excellent security practice, minimal information leakage  
- **httpbin.org**: `gunicorn/19.9.0` - Specific Python web server configuration
- **testphp.vulnweb.com**: `nginx/1.19.0` - Specific version disclosure on vulnerable test site (this wasn't included in the lab)

 Server headers help identify the software and version used and assessing security posture. The specific ones are good for research, but make it easy for attackers to exploit known vulnerabilities.

## Differences between the target sites in headers, titles, forms, and keywords.
### Headers:
- **Information Leakage**: scanme.nmap.org and httpbin.org revealed specific versions
- **Security Best Practices**: example.com showed excellent header security

### Titles & Forms:
- **scanme.nmap.org**: "Go ahead and ScanMe!" title with search forms at `/search/`
- **example.com**: Basic "Example Domain" with no forms
- **httpbin.org**: Simple title with no forms (API-focused)
- **testphp.vulnweb.com**: Multiple forms including login and search functionality

### Keywords:
- All sites showed `0` for admin, login, debug, and error keywords in visible text, which indicates good security hygiene with no exposed sensitive functionality.

## One defensive use of this information.

One key defensive measure that should could implemented:

**Minimize Server Header Information**: Configure web servers to remove or genericize server headers. Instead of `Apache/2.4.7 (Ubuntu)`, use just `Apache` or remove the header entirely. This reduces the attacks by not revealing specific versions that attackers can target with known vulnerabilities.

## Ethical precautions you must follow when performing similar reconnaissance.

When performing reconnaissance, several ethical precautions are essential:

1. **Only scan lab-provided hosts**: get written permission otherwise
2. Use conservative worker counts and timeouts
3. **Log everything: commands**: start/end times, targets, and outputs
5. **Responsible Disclosure**: If vulnerabilities are found accidentally, report them responsibly
6. **Educational Purpose**: Use skills for learning and improvement, not exploitation

