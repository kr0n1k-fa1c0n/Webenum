# WEBENUM - Web Enumeration Toolchain

**A Python-based reconnaissance script that chains ProjectDiscovery tools for web application testing preparation.**

```
╦ ╦╔═╗╔╗ ╔═╗╔╗╔╦ ╦╔╦╗
║║║║╣ ╠╩╗║╣ ║║║║ ║║║║
╚╩╝╚═╝╚═╝╚═╝╝╚╝╚═╝╩ ╩
Web Enumeration Toolchain v1.0
```

---

## 📖 Project Description

WEBENUM automates the reconnaissance phase of web application security testing by chaining multiple ProjectDiscovery tools:

**Pipeline Flow:**
```
Domain Input → subfinder → dnsx → naabu → httpx → katana → BurpSuite
```

**What it does:**
- Discovers subdomains
- Resolves live hosts
- Scans common web ports
- Probes HTTP/HTTPS services
- Crawls discovered URLs
- Generates BurpSuite-ready URL list

**Safety Note:** This tool performs ONLY reconnaissance and enumeration. No exploitation, brute-force, or destructive actions are performed.

---

## 🛠️ Dependencies

### Required Tools (ProjectDiscovery)

All of these must be installed before running the script:

1. **subfinder** - Subdomain discovery
2. **dnsx** - DNS resolution
3. **naabu** - Port scanning
4. **httpx** - HTTP probing
5. **katana** - Web crawling

### Python Requirements

- Python 3.6 or higher
- Standard library only (no extra packages needed for basic functionality)
- Optional: `openai` library for LLM analysis (bonus feature)

---

## 📦 Installation

### Step 1: Install ProjectDiscovery Tools

**On Linux/macOS:**
```bash
# Install Go (if not already installed)
wget https://go.dev/dl/go1.21.0.linux-amd64.tar.gz
sudo tar -C /usr/local -xzf go1.21.0.linux-amd64.tar.gz
export PATH=$PATH:/usr/local/go/bin

# Install all ProjectDiscovery tools
go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
go install -v github.com/projectdiscovery/dnsx/cmd/dnsx@latest
go install -v github.com/projectdiscovery/naabu/v2/cmd/naabu@latest
go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest
go install -v github.com/projectdiscovery/katana/cmd/katana@latest

# Add Go bin to PATH
export PATH=$PATH:~/go/bin
```

**On Windows:**
```powershell
# Install using winget or download from GitHub releases
# https://github.com/projectdiscovery
```

### Step 2: Set Up Python Script

```bash
# Clone or extract the project
cd EnumerationToolchain

# Make script executable (Linux/macOS)
chmod +x webenum.py

# Optional: Install dependencies for LLM feature
pip install -r requirements.txt
```

### Step 3: Verify Installation

```bash
# Check if all tools are available
./webenum.py -d example.com --dry-run
```

---

## 🚀 Usage

### Basic Usage

```bash
# Simple scan
./webenum.py -d example.com

# Specify output directory
./webenum.py -d example.com -o my_scan_results

# Test with dry-run (shows commands without executing)
./webenum.py -d example.com --dry-run
```

### BurpSuite Integration

**Method 1: Proxy-based (Recommended)**
```bash
# Route httpx and katana traffic through Burp
./webenum.py -d example.com -b 127.0.0.1:8080
```

**Setup in BurpSuite:**
1. Open BurpSuite
2. Go to Proxy → Options
3. Ensure proxy listener is active on 127.0.0.1:8080
4. Disable intercept (Proxy → Intercept → off)
5. Run the script with `-b 127.0.0.1:8080`
6. All traffic will appear in HTTP history

**Method 2: Import URLs**
```bash
# Generate URL list and import manually
./webenum.py -d example.com
# Then in BurpSuite:
# Target → Site map → Right-click → Import URLs
# Select: results/urls_for_burp.txt
```

### Advanced Usage

```bash
# Scan with custom output directory
./webenum.py -d target.com -o target_scan

# Scan with Burp proxy
./webenum.py -d target.com -b 127.0.0.1:8080 -o burp_scan

# Dry-run to preview commands
./webenum.py -d target.com --dry-run

# Bonus: LLM analysis of results
./webenum.py -d target.com --llm --llm-api-key sk-YOUR_OPENAI_KEY
```

---

## 📂 Output Files

After running the script, you'll find these files in the output directory:

| File | Description |
|------|-------------|
| `subfinder.txt` | All discovered subdomains |
| `dnsx.txt` | Resolved subdomains (live hosts) |
| `naabu.txt` | Hosts with open web ports |
| `httpx.txt` | Live HTTP/HTTPS services |
| `katana.txt` | Crawled URLs and endpoints |
| `urls_for_burp.txt` | Deduplicated URL list for BurpSuite |
| `summary.json` | JSON summary with statistics |

### Example Output Structure
```
results/
├── subfinder.txt       # 50 subdomains found
├── dnsx.txt           # 35 live hosts
├── naabu.txt          # 42 hosts with open ports
├── httpx.txt          # 38 HTTP services
├── katana.txt         # 250 crawled URLs
├── urls_for_burp.txt  # 288 unique URLs
└── summary.json       # Statistics and summary
```

---

## 🎯 Using Results in BurpSuite

### Option 1: Proxy Method (Live Capture)
1. Start BurpSuite and ensure proxy is on `127.0.0.1:8080`
2. Run: `./webenum.py -d target.com -b 127.0.0.1:8080`
3. Go to BurpSuite → Proxy → HTTP history
4. All requests will be logged automatically
5. Filter by domain to see target URLs

### Option 2: Import Method
1. Run: `./webenum.py -d target.com`
2. Open BurpSuite
3. Go to Target → Site map
4. Right-click in target list → "Paste URL"
5. Or use: Target → Site map → (right-click) → Import URLs
6. Select: `results/urls_for_burp.txt`

### What to Test Next
The script provides reconnaissance data. Manual testing should focus on:
- Login pages (`/login`, `/admin`)
- API endpoints (`/api/*`)
- Upload functionality (`/upload`)
- User input parameters
- Authentication mechanisms

---

## 🔍 Example Commands & Walkthroughs

### Example 1: Basic Scan
```bash
./webenum.py -d testphp.vulnweb.com -o example1
```

**Expected Output:**
```
╦ ╦╔═╗╔╗ ╔═╗╔╗╔╦ ╦╔╦╗
║║║║╣ ╠╩╗║╣ ║║║║ ║║║║
╚╩╝╚═╝╚═╝╚═╝╝╚╝╚═╝╩ ╩
Web Enumeration Toolchain v1.0

Target: testphp.vulnweb.com
Output: example1
==================================================

[*] Checking required tools...
[✓] subfinder found
[✓] dnsx found
[✓] naabu found
[✓] httpx found
[✓] katana found
[+] All tools are installed!

############################################################
# STEP 1: SUBDOMAIN ENUMERATION
############################################################
[WEBENUM] Finding subdomains with subfinder
...
```

### Example 2: With BurpSuite Proxy
```bash
# First, start BurpSuite and ensure proxy is running on 127.0.0.1:8080
./webenum.py -d example.com -b 127.0.0.1:8080 -o burp_test
```

### Example 3: Dry-Run
```bash
# Preview what will be executed
./webenum.py -d example.com --dry-run
```

---

## ⚠️ Safety and Legal Disclaimer

**IMPORTANT - READ CAREFULLY:**

1. **Authorization Required**: Only scan domains you own or have explicit written permission to test
2. **Reconnaissance Only**: This tool performs passive/active reconnaissance only
3. **No Exploitation**: No vulnerabilities are exploited
4. **Rate Limiting**: Tools may generate significant traffic
5. **Legal Compliance**: Unauthorized scanning may violate:
   - Computer Fraud and Abuse Act (USA)
   - Computer Misuse Act (UK)
   - Local cybersecurity laws

**By using this tool, you agree to:**
- Obtain proper authorization before scanning
- Use results responsibly
- Comply with all applicable laws
- Accept full responsibility for your actions

**The author assumes no liability for misuse of this tool.**

---

## 🐛 Troubleshooting

### "Tool not found" error
```bash
# Verify tools are in PATH
which subfinder dnsx naabu httpx katana

# If missing, reinstall or add to PATH
export PATH=$PATH:~/go/bin
```

### "Permission denied" error
```bash
# Make script executable
chmod +x webenum.py

# Or run with python directly
python3 webenum.py -d example.com
```

### No results found
- Check if target domain is valid
- Verify internet connectivity
- Some domains may have limited exposed infrastructure
- Try with a well-known domain first (e.g., `testphp.vulnweb.com`)

### BurpSuite proxy not working
- Ensure BurpSuite proxy is listening on specified address
- Disable intercept mode in BurpSuite
- Check firewall settings
- Verify proxy address format: `127.0.0.1:8080`

---

## 📊 Project Evaluation Checklist

✅ **Functionality (55%)**
- [x] Toolchain runs successfully
- [x] URLs file generated
- [x] Dry-run mode implemented
- [x] All 5 tools properly chained

✅ **Pipeline Quality (20%)**
- [x] Correct tool execution order
- [x] Safe defaults (reconnaissance only)
- [x] Results useful for BurpSuite

✅ **Documentation (15%)**
- [x] Complete README with usage
- [x] Safety disclaimers included
- [x] Example commands provided
- [x] Sample outputs included

✅ **Testing & Robustness (10%)**
- [x] Error handling implemented
- [x] Missing tool detection
- [x] Input validation
- [x] Graceful failures

🎁 **Bonus Features**
- [x] LLM integration (optional)
- [x] Colorized output
- [x] JSON summary generation
- [x] BurpSuite proxy support

---

## 📝 Sample Output

```
ENUMERATION SUMMARY
============================================================
Target: example.com
Time: 2025-11-20T14:30:00

Statistics:
  • subfinder: 45
  • dnsx: 38
  • naabu: 42
  • httpx: 35
  • katana: 187
============================================================

[✓] ENUMERATION COMPLETE!
Results location: results
BurpSuite import file: results/urls_for_burp.txt
```

---

## 🤝 Support

For issues or questions:
1. Review this README carefully
2. Check troubleshooting section
3. Verify all tools are properly installed
4. Contact course instructor if needed

---

## 📜 License

Educational use only - Azrieli School of Continuing Studies, Technion

---

**Version:** 1.0  
**Last Updated:** November 2025  
**Author:** Subhan Jafarov (Kron1k)
