#!/usr/bin/env python3
"""
WEBENUM - Web Enumeration Toolchain
A reconnaissance script for web application testing preparation
"""

import os
import sys
import argparse
import subprocess
import json
from pathlib import Path
from datetime import datetime
import shutil

# ASCII Banner
BANNER = """
╦ ╦╔═╗╔╗ ╔═╗╔╗╔╦ ╦╔╦╗
║║║║╣ ╠╩╗║╣ ║║║║ ║║║║
╚╩╝╚═╝╚═╝╚═╝╝╚╝╚═╝╩ ╩
Web Enumeration Toolchain v1.0
"""

class Colors:
    """ANSI color codes for terminal output"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'

class WebEnum:
    """Main enumeration class"""
    
    def __init__(self, args):
        self.domain = args.domain
        self.domain_file = args.file
        self.output_dir = args.output
        self.burp_proxy = args.burp_proxy
        self.dry_run = args.dry_run
        self.llm_analysis = args.llm
        self.llm_api_key = args.llm_api_key
        
        # Tool paths
        self.tools = {
            'subfinder': 'subfinder',
            'dnsx': 'dnsx',
            'naabu': 'naabu',
            'httpx': 'httpx',
            'katana': 'katana'
        }
        
        # Output files
        self.files = {
            'subfinder': 'subfinder.txt',
            'dnsx': 'dnsx.txt',
            'naabu': 'naabu.txt',
            'httpx': 'httpx.txt',
            'katana': 'katana.txt',
            'burp_urls': 'urls_for_burp.txt',
            'summary': 'summary.json'
        }
        
        # Setup output directory
        self.setup_output_dir()
        
    def setup_output_dir(self):
        """Create output directory structure"""
        if not self.dry_run:
            Path(self.output_dir).mkdir(parents=True, exist_ok=True)
            print(f"{Colors.GREEN}[+] Output directory created: {self.output_dir}{Colors.END}")
        else:
            print(f"{Colors.YELLOW}[DRY-RUN] Would create output directory: {self.output_dir}{Colors.END}")
    
    def print_banner(self):
        """Display ASCII banner"""
        print(f"{Colors.CYAN}{BANNER}{Colors.END}")
        print(f"{Colors.BOLD}Target: {Colors.END}{Colors.YELLOW}{self.domain or self.domain_file}{Colors.END}")
        print(f"{Colors.BOLD}Output: {Colors.END}{Colors.YELLOW}{self.output_dir}{Colors.END}")
        if self.burp_proxy:
            print(f"{Colors.BOLD}Burp Proxy: {Colors.END}{Colors.YELLOW}{self.burp_proxy}{Colors.END}")
        print("=" * 50)
        print()
    
    def check_tools(self):
        """Verify all required tools are installed"""
        print(f"{Colors.BLUE}[*] Checking required tools...{Colors.END}")
        missing_tools = []
        
        for tool_name, tool_cmd in self.tools.items():
            if not shutil.which(tool_cmd):
                missing_tools.append(tool_name)
                print(f"{Colors.RED}[!] {tool_name} not found{Colors.END}")
            else:
                print(f"{Colors.GREEN}[✓] {tool_name} found{Colors.END}")
        
        if missing_tools:
            print(f"\n{Colors.RED}[!] Missing tools: {', '.join(missing_tools)}{Colors.END}")
            print(f"{Colors.YELLOW}[!] Please install ProjectDiscovery tools from: https://github.com/projectdiscovery{Colors.END}")
            if not self.dry_run:
                sys.exit(1)
        else:
            print(f"{Colors.GREEN}[+] All tools are installed!{Colors.END}\n")
    
    def run_command(self, cmd, description, output_file=None):
        """Execute a command and handle output"""
        print(f"\n{Colors.CYAN}{'='*60}{Colors.END}")
        print(f"{Colors.BOLD}[WEBENUM] {description}{Colors.END}")
        print(f"{Colors.CYAN}{'='*60}{Colors.END}")
        
        cmd_str = ' '.join(cmd) if isinstance(cmd, list) else cmd
        print(f"{Colors.YELLOW}Command: {cmd_str}{Colors.END}")
        
        if output_file:
            output_path = os.path.join(self.output_dir, output_file)
            print(f"{Colors.YELLOW}Output: {output_path}{Colors.END}")
        
        if self.dry_run:
            print(f"{Colors.YELLOW}[DRY-RUN] Command not executed{Colors.END}")
            return True
        
        try:
            print(f"{Colors.GREEN}[+] Executing...{Colors.END}\n")
            
            if output_file:
                with open(os.path.join(self.output_dir, output_file), 'w') as f:
                    process = subprocess.Popen(
                        cmd,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True
                    )
                    
                    for line in process.stdout:
                        print(line.rstrip())
                        f.write(line)
                    
                    process.wait()
                    
                    if process.returncode != 0:
                        stderr = process.stderr.read()
                        print(f"{Colors.RED}[!] Error: {stderr}{Colors.END}")
                        return False
            else:
                result = subprocess.run(cmd, check=True, capture_output=True, text=True)
                print(result.stdout)
            
            print(f"{Colors.GREEN}[+] Completed successfully!{Colors.END}")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"{Colors.RED}[!] Error executing command: {e}{Colors.END}")
            return False
        except Exception as e:
            print(f"{Colors.RED}[!] Unexpected error: {e}{Colors.END}")
            return False
    
    def step1_subfinder(self):
        """Step 1: Subdomain enumeration with subfinder"""
        print(f"\n{Colors.HEADER}{'#'*60}{Colors.END}")
        print(f"{Colors.HEADER}# STEP 1: SUBDOMAIN ENUMERATION{Colors.END}")
        print(f"{Colors.HEADER}{'#'*60}{Colors.END}")
        
        cmd = ['subfinder', '-d', self.domain, '-all', '-silent']
        
        return self.run_command(
            cmd,
            "Finding subdomains with subfinder",
            self.files['subfinder']
        )
    
    def step2_dnsx(self):
        """Step 2: DNS resolution with dnsx"""
        print(f"\n{Colors.HEADER}{'#'*60}{Colors.END}")
        print(f"{Colors.HEADER}# STEP 2: DNS RESOLUTION{Colors.END}")
        print(f"{Colors.HEADER}{'#'*60}{Colors.END}")
        
        input_file = os.path.join(self.output_dir, self.files['subfinder'])
        
        if not self.dry_run and not os.path.exists(input_file):
            print(f"{Colors.RED}[!] Input file not found: {input_file}{Colors.END}")
            return False
        
        cmd = ['dnsx', '-l', input_file, '-silent']
        
        return self.run_command(
            cmd,
            "Resolving subdomains with dnsx",
            self.files['dnsx']
        )
    
    def step3_naabu(self):
        """Step 3: Port scanning with naabu"""
        print(f"\n{Colors.HEADER}{'#'*60}{Colors.END}")
        print(f"{Colors.HEADER}# STEP 3: PORT SCANNING{Colors.END}")
        print(f"{Colors.HEADER}{'#'*60}{Colors.END}")
        
        input_file = os.path.join(self.output_dir, self.files['dnsx'])
        
        if not self.dry_run and not os.path.exists(input_file):
            print(f"{Colors.RED}[!] Input file not found: {input_file}{Colors.END}")
            return False
        
        # Common web ports
        ports = '80,443,8080,8443,8000,8888,3000,5000'
        cmd = ['naabu', '-list', input_file, '-p', ports, '-silent']
        
        return self.run_command(
            cmd,
            "Scanning ports with naabu",
            self.files['naabu']
        )

    def step4_httpx(self):
        """Step 4: HTTP probing with httpx"""
        print(f"\n{Colors.HEADER}{'#' * 60}{Colors.END}")
        print(f"{Colors.HEADER}# STEP 4: HTTP PROBING{Colors.END}")
        print(f"{Colors.HEADER}{'#' * 60}{Colors.END}")

        input_file = os.path.join(self.output_dir, self.files['naabu'])

        if not self.dry_run and not os.path.exists(input_file):
            print(f"{Colors.RED}[!] Input file not found: {input_file}{Colors.END}")
            return False

        cmd = ['httpx', '-l', input_file, '-silent', '-follow-redirects']

        # BURP PROXY ÜÇÜN DÜZGÜN YOL (Go tool-ları üçün)
        if self.burp_proxy:
            cmd.extend(['-http-proxy', f'http://{self.burp_proxy}'])
            print(f"{Colors.YELLOW}[*] Burp proxy enabled: {self.burp_proxy} (via -http-proxy){Colors.END}")

        return self.run_command(
            cmd,
            "Probing HTTP services with httpx",
            self.files['httpx']
        )

    def step5_katana(self):
        """Step 5: Web crawling with katana"""
        print(f"\n{Colors.HEADER}{'#' * 60}{Colors.END}")
        print(f"{Colors.HEADER}# STEP 5: WEB CRAWLING{Colors.END}")
        print(f"{Colors.HEADER}{'#' * 60}{Colors.END}")

        input_file = os.path.join(self.output_dir, self.files['httpx'])

        if not self.dry_run and not os.path.exists(input_file):
            print(f"{Colors.RED}[!] Input file not found: {input_file}{Colors.END}")
            return False

        cmd = ['katana', '-list', input_file, '-silent', '-d', '3']

        # BURP PROXY ÜÇÜN DÜZGÜN YOL (Go tool-ları üçün)
        if self.burp_proxy:
            cmd.extend(['-proxy', f'http://{self.burp_proxy}'])
            print(f"{Colors.YELLOW}[*] Burp proxy enabled: {self.burp_proxy} (via -proxy){Colors.END}")

        return self.run_command(
            cmd,
            "Crawling URLs with katana",
            self.files['katana']
        )
    
    def generate_burp_urls(self):
        """Generate a clean URL list for BurpSuite import"""
        print(f"\n{Colors.CYAN}[*] Generating BurpSuite URL list...{Colors.END}")
        
        if self.dry_run:
            print(f"{Colors.YELLOW}[DRY-RUN] Would generate {self.files['burp_urls']}{Colors.END}")
            return
        
        urls = set()
        
        # Collect from httpx
        httpx_file = os.path.join(self.output_dir, self.files['httpx'])
        if os.path.exists(httpx_file):
            with open(httpx_file, 'r') as f:
                urls.update(line.strip() for line in f if line.strip())
        
        # Collect from katana
        katana_file = os.path.join(self.output_dir, self.files['katana'])
        if os.path.exists(katana_file):
            with open(katana_file, 'r') as f:
                urls.update(line.strip() for line in f if line.strip())
        
        # Write to burp URLs file
        burp_file = os.path.join(self.output_dir, self.files['burp_urls'])
        with open(burp_file, 'w') as f:
            for url in sorted(urls):
                f.write(f"{url}\n")
        
        print(f"{Colors.GREEN}[+] BurpSuite URL list created: {burp_file}{Colors.END}")
        print(f"{Colors.GREEN}[+] Total unique URLs: {len(urls)}{Colors.END}")
    
    def generate_summary(self):
        """Generate a JSON summary of findings"""
        print(f"\n{Colors.CYAN}[*] Generating summary...{Colors.END}")
        
        if self.dry_run:
            print(f"{Colors.YELLOW}[DRY-RUN] Would generate {self.files['summary']}{Colors.END}")
            return
        
        summary = {
            'target': self.domain,
            'timestamp': datetime.now().isoformat(),
            'statistics': {},
            'findings': {}
        }
        
        # Count results from each file
        for key, filename in self.files.items():
            if key in ['burp_urls', 'summary']:
                continue
            
            filepath = os.path.join(self.output_dir, filename)
            if os.path.exists(filepath):
                with open(filepath, 'r') as f:
                    lines = [line.strip() for line in f if line.strip()]
                    summary['statistics'][key] = len(lines)
                    summary['findings'][key] = lines[:10]  # First 10 entries
        
        # Write summary
        summary_file = os.path.join(self.output_dir, self.files['summary'])
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"{Colors.GREEN}[+] Summary created: {summary_file}{Colors.END}")
        self.print_summary(summary)
    
    def print_summary(self, summary):
        """Print summary statistics"""
        print(f"\n{Colors.HEADER}{'='*60}{Colors.END}")
        print(f"{Colors.HEADER}ENUMERATION SUMMARY{Colors.END}")
        print(f"{Colors.HEADER}{'='*60}{Colors.END}")
        print(f"{Colors.BOLD}Target:{Colors.END} {summary['target']}")
        print(f"{Colors.BOLD}Time:{Colors.END} {summary['timestamp']}")
        print(f"\n{Colors.BOLD}Statistics:{Colors.END}")
        
        for key, count in summary['statistics'].items():
            print(f"  {Colors.CYAN}• {key}:{Colors.END} {Colors.YELLOW}{count}{Colors.END}")
        
        print(f"{Colors.HEADER}{'='*60}{Colors.END}\n")
    
    def llm_analyze(self):
        """Optional: Analyze results with LLM"""
        if not self.llm_analysis or not self.llm_api_key:
            return
        
        print(f"\n{Colors.HEADER}{'#'*60}{Colors.END}")
        print(f"{Colors.HEADER}# BONUS: LLM ANALYSIS{Colors.END}")
        print(f"{Colors.HEADER}{'#'*60}{Colors.END}")
        
        if self.dry_run:
            print(f"{Colors.YELLOW}[DRY-RUN] Would perform LLM analysis{Colors.END}")
            return
        
        print(f"{Colors.YELLOW}[*] Analyzing endpoints with LLM...{Colors.END}")
        
        try:
            import openai
            openai.api_key = self.llm_api_key
            
            # Read URLs
            burp_file = os.path.join(self.output_dir, self.files['burp_urls'])
            with open(burp_file, 'r') as f:
                urls = [line.strip() for line in f if line.strip()]
            
            prompt = f"""Analyze these URLs from web enumeration and identify high-value endpoints for security testing:

{chr(10).join(urls[:50])}

Provide a JSON response with:
- high_value_endpoints: list of URLs that might have security issues (login, admin, upload, api)
- interesting_parameters: URLs with query parameters
- priority_targets: top 5 URLs to test first

Focus on reconnaissance value only, no exploitation."""

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3
            )
            
            analysis = response.choices[0].message.content
            
            # Save analysis
            analysis_file = os.path.join(self.output_dir, 'llm_analysis.json')
            with open(analysis_file, 'w') as f:
                f.write(analysis)
            
            print(f"{Colors.GREEN}[+] LLM analysis saved: {analysis_file}{Colors.END}")
            
        except ImportError:
            print(f"{Colors.RED}[!] OpenAI library not installed. Run: pip install openai{Colors.END}")
        except Exception as e:
            print(f"{Colors.RED}[!] LLM analysis failed: {e}{Colors.END}")
    
    def run(self):
        """Execute the complete enumeration pipeline"""
        self.print_banner()
        
        # Check if tools are installed
        self.check_tools()
        
        # Execute pipeline
        if not self.step1_subfinder():
            print(f"{Colors.RED}[!] Subfinder failed, stopping pipeline{Colors.END}")
            return False
        
        if not self.step2_dnsx():
            print(f"{Colors.RED}[!] dnsx failed, stopping pipeline{Colors.END}")
            return False
        
        if not self.step3_naabu():
            print(f"{Colors.RED}[!] naabu failed, stopping pipeline{Colors.END}")
            return False
        
        if not self.step4_httpx():
            print(f"{Colors.RED}[!] httpx failed, stopping pipeline{Colors.END}")
            return False
        
        if not self.step5_katana():
            print(f"{Colors.RED}[!] katana failed, stopping pipeline{Colors.END}")
            return False
        
        # Generate outputs
        self.generate_burp_urls()
        self.generate_summary()
        
        # Optional LLM analysis
        self.llm_analyze()
        
        # Final message
        print(f"\n{Colors.GREEN}{'='*60}{Colors.END}")
        print(f"{Colors.GREEN}[✓] ENUMERATION COMPLETE!{Colors.END}")
        print(f"{Colors.GREEN}{'='*60}{Colors.END}")
        print(f"\n{Colors.BOLD}Results location:{Colors.END} {Colors.YELLOW}{self.output_dir}{Colors.END}")
        print(f"{Colors.BOLD}BurpSuite import file:{Colors.END} {Colors.YELLOW}{os.path.join(self.output_dir, self.files['burp_urls'])}{Colors.END}")
        
        return True


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='WEBENUM - Web Enumeration Toolchain for BurpSuite preparation',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s -d example.com
  %(prog)s -d example.com -o results -b 127.0.0.1:8080
  %(prog)s -d example.com --dry-run
  %(prog)s -f domains.txt -o scan_results
  %(prog)s -d example.com --llm --llm-api-key YOUR_KEY
        """
    )
    
    # Required arguments
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument('-d', '--domain', help='Target domain (e.g., example.com)')
    input_group.add_argument('-f', '--file', help='File with domains (one per line)')
    
    # Optional arguments
    parser.add_argument('-o', '--output', default='results', 
                       help='Output directory (default: results)')
    parser.add_argument('-b', '--burp-proxy', 
                       help='BurpSuite proxy address (e.g., 127.0.0.1:8080)')
    parser.add_argument('--dry-run', action='store_true',
                       help='Show commands without executing')
    parser.add_argument('--llm', action='store_true',
                       help='Enable LLM analysis (bonus feature)')
    parser.add_argument('--llm-api-key',
                       help='OpenAI API key for LLM analysis')
    
    args = parser.parse_args()
    
    # Handle file input
    if args.file:
        print(f"{Colors.YELLOW}[!] Multi-domain scanning not yet implemented{Colors.END}")
        print(f"{Colors.YELLOW}[!] Please scan one domain at a time{Colors.END}")
        sys.exit(1)
    
    # Create and run enumerator
    try:
        enumerator = WebEnum(args)
        success = enumerator.run()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}[!] Interrupted by user{Colors.END}")
        sys.exit(1)
    except Exception as e:
        print(f"{Colors.RED}[!] Fatal error: {e}{Colors.END}")
        sys.exit(1)


if __name__ == '__main__':
    main()
