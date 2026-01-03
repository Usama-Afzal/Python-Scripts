# NACTA Pakistan File Automation 🇵🇰

This production-grade script automates the retrieval of **Notified** and **De-notified** Proscribed Persons lists from NACTA Pakistan. 

### Why this tool?
NACTA transitioned from static links to dynamic web elements, breaking traditional `curl` or `wget` methods. This tool uses **Selenium** to handle the dynamic frontend, ensuring your compliance databases are always in sync.

### Security & Compliance
- **Zero Hardcoding:** All IPs, paths, and credentials are isolated in a `.env` file (not included in the repo for security).
- **Process Integrity:** Automatically manages and cleans up Chrome/Driver processes to ensure server stability.
- **Encrypted Sync:** Uses Rsync over SSH with custom port and key support.

### Setup
1. `pip install -r requirements.txt`
2. Configure your `.env` file using the provided template.
3. Run `python nacta_sync.py`.

*Note: For feedback, bug reports, or feature requests, please reach out to the project maintainer.*
