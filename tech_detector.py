"""
tech_detector.py
Enter a website URL. Reports publicly available info: DNS records,
HTTP headers, and technology hints (CMS, server, analytics, etc.)
detectable from response headers and page content.

Only uses information any browser visiting the site would also see --
this is passive, publicly available data, not a scan of anything private.
"""

import requests
import socket


def get_dns_info(domain: str) -> dict:
    try:
        ip = socket.gethostbyname(domain)
    except socket.gaierror:
        ip = "Could not resolve"
    return {"domain": domain, "ip_address": ip}


def get_headers_and_tech(url: str) -> dict:
    if not url.startswith("http"):
        url = "https://" + url

    try:
        response = requests.get(url, timeout=10)
    except requests.RequestException as e:
        return {"error": str(e)}

    headers = dict(response.headers)
    html = response.text.lower()

    tech_hints = []
    if "wordpress" in html or "wp-content" in html:
        tech_hints.append("WordPress")
    if "shopify" in html:
        tech_hints.append("Shopify")
    if "react" in html or "__next" in html:
        tech_hints.append("React / Next.js")
    if "vue" in html:
        tech_hints.append("Vue.js")
    if "cloudflare" in str(headers.get("Server", "")).lower():
        tech_hints.append("Cloudflare (CDN/proxy)")
    if "x-powered-by" in headers:
        tech_hints.append(f"Powered by: {headers['x-powered-by']}")

    return {
        "status_code": response.status_code,
        "server": headers.get("Server", "Unknown"),
        "content_type": headers.get("Content-Type", "Unknown"),
        "technologies_detected": tech_hints or ["None detected from headers/content"],
        "headers": headers,
    }


def scan(url: str):
    domain = url.replace("https://", "").replace("http://", "").split("/")[0]

    print(f"\nScanning {domain} ...\n")
    dns_info = get_dns_info(domain)
    print("DOMAIN INFO")
    print(f"  IP Address: {dns_info['ip_address']}\n")

    tech_info = get_headers_and_tech(url)
    if "error" in tech_info:
        print(f"Error: {tech_info['error']}")
        return

    print("SERVER INFO")
    print(f"  Server: {tech_info['server']}")
    print(f"  Status: {tech_info['status_code']}")
    print(f"  Content-Type: {tech_info['content_type']}\n")

    print("TECHNOLOGIES DETECTED")
    for tech in tech_info["technologies_detected"]:
        print(f"  - {tech}")


if __name__ == "__main__":
    target = input("Enter a website (e.g. example.com): ").strip()
    scan(target)
