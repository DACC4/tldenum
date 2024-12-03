import dns.resolver
import whois
import logging
import requests
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

# Suppress whois library logging errors
logging.getLogger("whois").setLevel(logging.CRITICAL)

def fetch_tlds():
    """Fetch the list of TLDs from IANA."""
    url = "https://data.iana.org/TLD/tlds-alpha-by-domain.txt"
    response = requests.get(url)
    if response.status_code == 200:
        tlds = response.text.splitlines()
        return [tld.lower() for tld in tlds if not tld.startswith("#")]
    else:
        raise Exception(f"Failed to fetch TLDs: {response.status_code}")

def check_via_whois(domain):
    """Check if a domain is registered using the local whois library."""
    try:
        w = whois.whois(domain)
        if w.status:  # If a status is present, the domain is registered
            return {
                "method": "whois",
                "registrar": w.get("registrar"),
                "registrant": w.get("registrant_name"),
                "creation_date": str(w.get("creation_date")),
                "expiration_date": str(w.get("expiration_date")),
            }
    except Exception:
        pass
    return None

def check_via_txt_dns(domain):
    """Check if a domain resolves via DNS TXT records."""
    try:
        # Query TXT records for the domain
        answers = dns.resolver.resolve(domain, 'TXT')
        txt_records = [r.to_text() for r in answers]
        if txt_records:
            return {
                "method": "txt_dns",
                "txt_records": txt_records
            }
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.resolver.Timeout):
        pass
    return None

def check_domain_registration(domain):
    """Check if a domain is registered using multiple methods."""
    # Check using local whois
    whois_result = check_via_whois(domain)
    if whois_result:
        return whois_result

    # Fallback: Check if the domain resolves via DNS TXT records
    dns_result = check_via_txt_dns(domain)
    if dns_result:
        return dns_result

    return None

def process_domain(base_name, tld):
    """Process a single domain."""
    domain = f"{base_name}.{tld}"
    result = check_domain_registration(domain)
    return domain, result

def enumerate_domains(base_name, tlds, max_threads=10):
    """Enumerate all possible domains for a base name with the given TLDs using multithreading."""
    results = {}
    with ThreadPoolExecutor(max_threads) as executor:
        futures = {executor.submit(process_domain, base_name, tld): tld for tld in tlds}
        with tqdm(total=len(tlds), desc="Checking domains", unit="domain") as pbar:
            for future in as_completed(futures):
                domain, result = future.result()
                if result:
                    print(f"FOUND REGISTERED: {domain} (method: {result['method']})")
                    results[domain] = {"registered": True, "details": result}
                else:
                    results[domain] = {"registered": False}
                pbar.set_description(f"Checked {domain}")
                pbar.update(1)
    return results

def save_to_yaml(data, file_name="output.yaml"):
    """Save the results to a YAML file."""
    import yaml
    with open(file_name, "w") as file:
        yaml.dump(data, file, default_flow_style=False)
    print(f"Results saved to {file_name}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Enumerate TLDs for a company name and check registration.")
    parser.add_argument("company_name", type=str, help="The base company name (e.g., example)")
    parser.add_argument("--threads", type=int, default=10, help="Number of threads to use (default: 10)")
    args = parser.parse_args()

    base_name = args.company_name.lower().strip()

    try:
        print("Fetching TLDs...")
        tlds = fetch_tlds()
        print(f"Fetched {len(tlds)} TLDs.")
        
        print("Enumerating domains...")
        results = enumerate_domains(base_name, tlds, max_threads=args.threads)
        
        print("Saving results to YAML...")
        save_to_yaml(results)
    except Exception as e:
        print(f"Error: {e}")
