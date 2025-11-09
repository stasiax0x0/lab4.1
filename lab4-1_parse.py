#!/usr/bin/env python3
# lab4-1_parse.py
# Phase 2 told us "what server software is running," Phase 3 tells us "what the application actually does."
from bs4 import BeautifulSoup
import requests, json, sys, urllib.parse

def parse_page(url, out_file=None):                 #Fetches the webpage and creates a BeautifulSoup object that lets us navigate and search the HTML structure like a browser would.
    r = requests.get(url, timeout=5)
    soup = BeautifulSoup(r.text, "html.parser")

    title = soup.title.string.strip() if soup.title and soup.title.string else None     #Gets the text between <title> tags (what appears in browser tabs. Titles reveal the page's purpose and sometimes application names
    meta = soup.find("meta", attrs={"name": "description"})                             #ooks for <meta name="description"> tags used for SEO
    meta_desc = meta["content"].strip() if meta and meta.get("content") else None       #Meta descriptions can reveal business logic or functionality

#form extraction
    forms = []
    for f in soup.find_all("form"):                                 #finds every form element on the page
        method = f.get("method", "GET").upper()                     #extracts the HTTP method (get/post-) 
        action = urllib.parse.urljoin(url, f.get("action", ""))     #resolvess the action URL, where the form submits data
        inputs = []                                                 #lists all input fields, so the data the form collects. Show what parameters can be manipulated
        for inp in f.find_all("input"):
            inputs.append({
                "name": inp.get("name"),
                "type": inp.get("type"),
                "value": inp.get("value")
            })
        forms.append({"method": method, "action": action, "inputs": inputs})

    result = {
        "url": url,
        "title": title,
        "meta_description": meta_desc,
        "forms": forms
    }
    #keyword scanning (added in 3.2)
    keywords = ["admin", "login", "debug", "error"]         #the keywords we're looking for
    text = soup.get_text(separator=" ").lower()             #takes the whole text and turns it to lowercase
    kw_counts = {k: text.count(k) for k in keywords}        #counts how many times a keyword appears
    result["keyword_counts"] = kw_counts

    if out_file:
        with open(out_file, "w") as fh:
            json.dump(result, fh, indent=2)
    print(json.dumps(result, indent=2))
    return result

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python lab1_parse.py <url> [out_file.json]")
        sys.exit(1)
    parse_page(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)