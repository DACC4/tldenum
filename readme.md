# Domain Enumerator and Reporter

A Python-based project to enumerate and validate domain registrations across various TLDs (Top-Level Domains). The project uses `whois` and DNS `TXT` record lookups to determine if a domain is registered and provides detailed reports on the results.

---

## Features

- **Enumerates Domains Across TLDs**:
  - Automatically fetches the list of all TLDs from [IANA's TLD database](https://data.iana.org/TLD/tlds-alpha-by-domain.txt).
  - Generates domain combinations for a given base name and checks their registration status.

- **Multi-Source Validation**:
  - Uses `whois` to check domain registration and retrieve detailed information (registrar, creation/expiration dates, etc.).
  - Fallback to DNS `TXT` record lookups to detect active domains.

- **Multithreaded for Speed**:
  - Leverages multithreading to process multiple domains concurrently, improving performance.

- **Detailed Reports**:
  - Outputs results in YAML format, including detection method and relevant details for each registered domain.
  - Provides a formatted console report for quick insights.

- **Robust Error Handling**:
  - Handles `None` or missing data gracefully.
  - Filters out incomplete or invalid entries for a cleaner output.

---

## Requirements

- Python 3.8 or later
- Dependencies:
  - `python-whois`
  - `dnspython`
  - `tqdm`
  - `pyyaml`

---

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/domain-enumerator.git
   cd domain-enumerator
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

### 1. **Domain Enumeration**
The `enumerate_tlds.py` script generates a list of domains for a given base name and checks their registration status.

#### Example Command:
```bash
python enumerate_tlds.py example --threads 20
```

#### Options:
- `company_name` (required): The base name to use for domain generation (e.g., `example`).
- `--threads` (optional): Number of threads to use for multithreaded processing (default: 10).

#### Output:
- Results are saved to `output.yaml` by default.
- Found domains are logged in real time to the console:
  ```
  FOUND REGISTERED: example.com (method: whois)
  ```

### 2. **Report Generation**
The `report.py` script parses the YAML file and generates a console-friendly report of all registered domains.

#### Example Command:
```bash
python report.py output.yaml
```

#### Features:
- Filters out incomplete or invalid entries (e.g., domains with no meaningful `whois` or DNS data).
- Displays a detailed table of registered domains, including the detection method and relevant details.

#### Sample Output:
```
Domain                          Method     Registrar                      Registrant                     Creation Date       Expiration Date      TXT Records
============================================================================================================================================================
example.com                     whois      Example Registrar              John Doe                      2000-01-01 00:00:00 2025-01-01 00:00:00 
example.net                     txt_dns    N/A                            N/A                           N/A                 N/A                 v=spf1 include:_spf.google.com ~all
```

---

## File Structure

```
domain-enumerator/
├── enumerate_tlds.py  # Main script for domain enumeration
├── report.py          # Script for generating reports
├── requirements.txt   # Dependencies
├── README.md          # Project documentation
└── output.yaml        # Sample output file (generated after running `enumerate_tlds.py`)
```

---

## Example Workflow

1. **Run Domain Enumeration**:
   ```bash
   python enumerate_tlds.py example
   ```
   Output is saved to `output.yaml`.

2. **Generate and View Report**:
   ```bash
   python report.py output.yaml
   ```

3. **Sample YAML File**:
   ```yaml
   example.com:
     registered: true
     details:
       method: whois
       registrar: Example Registrar
       registrant: John Doe
       creation_date: '2000-01-01 00:00:00'
       expiration_date: '2025-01-01 00:00:00'
   example.net:
     registered: true
     details:
       method: txt_dns
       txt_records:
       - "v=spf1 include:_spf.google.com ~all"
   example.xyz:
     registered: false
   ```

---

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests to enhance the project.

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Commit your changes and submit a pull request.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Acknowledgments

- [IANA TLD List](https://data.iana.org/TLD/tlds-alpha-by-domain.txt)
- Python libraries: `whois`, `dnspython`, `tqdm`, `pyyaml`