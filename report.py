import yaml
import argparse

def parse_yaml(file_name):
    """Parse the YAML file and return the data."""
    try:
        with open(file_name, "r") as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        print(f"Error: File {file_name} not found.")
        return None
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")
        return None

def safe_get(value, default="N/A"):
    """Return the value if not None, otherwise return the default."""
    return value if value is not None else default

def is_valid_entry(details):
    """Validate if an entry has meaningful information."""
    if details.get("method") == "whois":
        # If whois is the method, require at least one meaningful field
        registrar = details.get("registrar")
        registrant = details.get("registrant")
        return registrar is not None or registrant is not None
    elif details.get("method") == "txt_dns":
        # If txt_dns is the method, require at least one TXT record
        txt_records = details.get("txt_records")
        return txt_records and len(txt_records) > 0
    return False

def extract_registered_domains(data):
    """Extract and format information about registered domains."""
    registered_domains = []
    for domain, info in data.items():
        if info.get("registered"):
            details = info.get("details", {})
            if is_valid_entry(details):
                method = safe_get(details.get("method"))
                if method == "whois":
                    registered_domains.append({
                        "domain": domain,
                        "method": "whois",
                        "registrar": safe_get(details.get("registrar")),
                        "registrant": safe_get(details.get("registrant")),
                        "creation_date": safe_get(details.get("creation_date")),
                        "expiration_date": safe_get(details.get("expiration_date")),
                    })
                elif method == "txt_dns":
                    registered_domains.append({
                        "domain": domain,
                        "method": "txt_dns",
                        "txt_records": safe_get(details.get("txt_records"), []),
                    })
    return registered_domains

def display_registered_domains(domains):
    """Display the registered domains in a formatted output."""
    if not domains:
        print("No registered domains found.")
        return

    print(f"\n{'Domain':<30} {'Method':<10} {'Registrar':<30} {'Registrant':<30} {'Creation Date':<20} {'Expiration Date':<20} TXT Records")
    print("=" * 150)
    for domain_info in domains:
        if domain_info["method"] == "whois":
            print(
                f"{domain_info['domain']:<30} "
                f"{domain_info['method']:<10} "
                f"{domain_info['registrar']:<30} "
                f"{domain_info['registrant']:<30} "
                f"{domain_info['creation_date']:<20} "
                f"{domain_info['expiration_date']:<20} "
            )
        elif domain_info["method"] == "txt_dns":
            txt_records = ", ".join(domain_info["txt_records"])
            print(
                f"{domain_info['domain']:<30} "
                f"{domain_info['method']:<10} "
                f"{'N/A':<30} "
                f"{'N/A':<30} "
                f"{'N/A':<20} "
                f"{'N/A':<20} "
                f"{txt_records}"
            )

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse YAML file and display registered domains.")
    parser.add_argument("file", type=str, help="Path to the YAML file containing domain data")
    args = parser.parse_args()

    data = parse_yaml(args.file)
    if data:
        registered_domains = extract_registered_domains(data)
        display_registered_domains(registered_domains)
