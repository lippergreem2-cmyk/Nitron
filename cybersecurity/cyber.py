# cyber.py

from linux_helper import explain_command
from password_audit import check_password
from security_advisor import security_tips
from network_tools import network_info
from port_scanner import scan_host
from log_analyzer import analyze_log
from wifi_tools import wifi_info
from ctf_tools import ctf_help


class Cyber:

    def __init__(self):
        self.name = "Nitron Cyber"

    def banner(self):

        print("=" * 70)
        print("            NITRON CYBER SECURITY SUITE")
        print("=" * 70)
        print("Modules Loaded")
        print("- Linux Helper")
        print("- Password Auditor")
        print("- Network Tools")
        print("- Port Scanner")
        print("- WiFi Tools")
        print("- Log Analyzer")
        print("- Security Advisor")
        print("- CTF Helper")
        print("=" * 70)

    def help(self):

        print("""
Commands

help
linux <command>
password <password>
network
scan <host>
wifi
log <file>
tips
ctf
clear
about
exit
""")

    def run(self):

        self.banner()

        while True:

            command = input("Nitron-Cyber> ").strip()

            if command == "":
                continue

            elif command.lower() == "exit":
                print("Shutting down Nitron Cyber...")
                break

            elif command.lower() == "help":
                self.help()

            elif command.lower() == "about":
                print("""
Nitron Cyber Security Suite

Version : 1.0

Modules
--------
Linux Assistant
Password Auditor
Network Inspector
Port Scanner
WiFi Inspector
Log Analyzer
Security Advisor
CTF Practice
""")

            elif command.lower() == "clear":
                print("\n" * 50)

            elif command.lower().startswith("linux "):
                print(explain_command(command[6:]))

            elif command.lower().startswith("password "):
                print(check_password(command[9:]))

            elif command.lower() == "network":
                print(network_info())

            elif command.lower().startswith("scan "):
                print(scan_host(command[5:]))

            elif command.lower() == "wifi":
                print(wifi_info())

            elif command.lower().startswith("log "):
                print(analyze_log(command[4:]))

            elif command.lower() == "tips":
                print(security_tips())

            elif command.lower() == "ctf":
                ctf_help()

            else:
                print("Unknown command. Type help.")

if __name__ == "__main__":
    Cyber().run()
