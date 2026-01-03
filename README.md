# 🛠️ Python-Scripts: DevOps & Automation Collection

Welcome to my repository of Python-driven automation solutions. This collection is focused on solving real-world infrastructure challenges, data compliance hurdles, and streamlining repetitive tasks using a "DevOps-First" approach.

---

## 📂 Repository Structure

Each project is contained within its own directory with dedicated documentation and environment configurations.

| Project Name | Description | Status |
| :--- | :--- | :--- |
| [**NACTA Automation**](./Nacta-Automation) | Automates the retrieval and syncing of proscribed lists via Selenium & Rsync. | ✅ Active |
| *More coming soon* | *Additional automation tools and cloud scripts...* | ⏳ Pending |

---

## 🌟 Featured Project: NACTA Automation

### The Problem
Government portals (like NACTA Pakistan) often transition from static file APIs to dynamic, JavaScript-heavy frontends. This makes traditional data scraping or `curl` commands obsolete.

### The Solution
A robust, production-grade automation engine that:
* **Simulates Human Interaction:** Uses **Selenium** to navigate dynamic web elements.
* **Infrastructure Sync:** Automatically pushes downloaded assets to remote servers using **Rsync**.
* **Proactive Monitoring:** Features a dual-channel notification system (Slack Webhooks + SMTP Email).
* **Enterprise-Grade Security:** Implements `.env` isolation for all sensitive credentials (IPs, Ports, API Keys).

---

## 🛡️ Security & Best Practices

As a DevOps Engineer, security and stability are my priorities:
1.  **Secret Management:** No credentials are ever hardcoded. All scripts load sensitive data via `python-dotenv`.
2.  **Resource Hygiene:** Scripts include automated cleanup of Chrome and ChromeDriver processes to prevent memory leaks.
3.  **Modular Design:** Everything is built to be plug-and-play for your own infrastructure.

---

## 🛠️ General Prerequisites

To run the scripts in this repository, you generally need:
* **Python 3.8+**
* **Google Chrome & ChromeDriver** (for web automation)
* **Rsync / SSH Access** (for remote synchronization)

---

## 🤝 Contribution & Feedback

I am constantly refining these tools. If you:
* Find a bug 🐛
* Have a feature request 🚀
* Want to suggest a more secure approach 🛡️

Please feel free to **ping me** or open a **Pull Request**. Let's build better automation tools together!

---

**Maintained by:** [Usama Muhammad Afzal]  
**Location:** Karachi, Pakistan 🇵🇰
