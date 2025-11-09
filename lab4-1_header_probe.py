#!/usr/bin/env python3
# lab4-1_header_probe.py
#Testing how servers respond to different "User-Agent" strings to detect security systems and fingerprint protection mechanisms.


import requests, sys, csv

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",        #regular browser
    "curl/7.68.0",                                      #command line tool
    "sqlmap/1.5.4",                                     #sql injection tool
    "Nikto/2.1.6",                                      #web vulnerability scanner
    "python-requests/2.x"                               #python library
]

def probe(url, out_csv=None):                           #probe is the main testing function, url is the website we're testing and out_csv is an optional filename to save results
    rows = []                                           #empty list to store results
    for ua in USER_AGENTS:                              #loop through each user-agent
        headers = {"User-Agent": ua}
        try:
            r = requests.get(url, headers=headers, timeout=5)       #tries to visit the website with the fake user-agent and if susccessful it will record the following info
            rows.append({
                "ua": ua,
                "status": r.status_code,
                "server": r.headers.get("Server", ""),
                "length": len(r.text)
            })
        except requests.exceptions.RequestException as e:               #if the requests fails , it will record the error instead of crashing
            rows.append({"ua": ua, "error": str(e)})

    # Test 1: X-Forwarded-For
    try:
        headers = {"User-Agent": "Mozilla/5.0", "X-Forwarded-For": "1.2.3.4"}
        r = requests.get(url, headers=headers, timeout=5)
        rows.append({
            "ua": "TEST: X-Forwarded-For: 1.2.3.4",
            "status": r.status_code,
            "server": r.headers.get("Server", ""),
            "length": len(r.text)
        })
    except Exception as e:
        rows.append({"ua": "TEST: X-Forwarded-For: 1.2.3.4", "error": str(e)})
    
    # Test 2: Referer
    try:
        headers = {"User-Agent": "Mozilla/5.0", "Referer": "http://evil.example/"}
        r = requests.get(url, headers=headers, timeout=5)
        rows.append({
            "ua": "TEST: Referer: http://evil.example/",
            "status": r.status_code,
            "server": r.headers.get("Server", ""),
            "length": len(r.text)
        })
    except Exception as e:
        rows.append({"ua": "TEST: Referer: http://evil.example/", "error": str(e)})
    
    # Test 3: Accept-Language
    try:
        headers = {"User-Agent": "Mozilla/5.0", "Accept-Language": "fr-FR"}
        r = requests.get(url, headers=headers, timeout=5)
        rows.append({
            "ua": "TEST: Accept-Language: fr-FR", 
            "status": r.status_code,
            "server": r.headers.get("Server", ""),
            "length": len(r.text)
        })
    except Exception as e:
        rows.append({"ua": "TEST: Accept-Language: fr-FR", "error": str(e)})


    if out_csv:                                                         #saving the results
        with open(out_csv, "w", newline='') as fh:
            writer = csv.DictWriter(fh, fieldnames=["ua","status","server","length","error"])
            writer.writeheader()
            for r in rows:
                writer.writerow(r)
    for r in rows:
        print(r)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python lab1_header_probe.py <url> [out.csv]")
        sys.exit(1)
    probe(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)