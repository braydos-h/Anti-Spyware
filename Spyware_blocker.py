import tkinter as tk
from tkinter import messagebox, scrolledtext
import subprocess
import requests
import ctypes
import sys
import datetime

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def download_ips(url):
    response = requests.get(url)
    response.raise_for_status()
    ips = response.text.splitlines()
    return [ip for ip in ips if ip and not ip.startswith("#")]

def block_ips_with_firewall(ips, log_widget):
    for ip in ips:
        log_widget.insert(tk.END, f"Blocking IP: {ip}\n")
        log_widget.see(tk.END)
        log_widget.update()
        subprocess.run(["netsh", "advfirewall", "firewall", "add", "rule", 
                        f"name=Block {ip}", "dir=out", "action=block", f"remoteip={ip}"])
    log_widget.insert(tk.END, "Finished blocking IP addresses.\n")

def modify_privacy_settings(log_widget):
    log_widget.insert(tk.END, "Disabling Cortana...\n")
    subprocess.run(["reg", "add", "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\Windows Search", "/v", "AllowCortana", "/t", "REG_DWORD", "/d", "0", "/f"])
    log_widget.insert(tk.END, "Disabling telemetry...\n")
    subprocess.run(["reg", "add", "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\DataCollection", "/v", "AllowTelemetry", "/t", "REG_DWORD", "/d", "0", "/f"])
    log_widget.insert(tk.END, "Finished modifying privacy settings.\n")

def clear_browser_data(log_widget):
    log_widget.insert(tk.END, "Clearing browser data...\n")
    browsers = ["chrome", "firefox", "edge"]
    for browser in browsers:
        subprocess.run([browser, "--clear-browsing-data=all"])
    log_widget.insert(tk.END, "Finished clearing browser data.\n")

def disable_unnecessary_services(log_widget):
    log_widget.insert(tk.END, "Disabling unnecessary services...\n")
    services = ["DiagTrack", "dmwappushservice"]
    for service in services:
        subprocess.run(["sc", "config", service, "start=", "disabled"])
    log_widget.insert(tk.END, "Finished disabling unnecessary services.\n")

def block_ads_and_trackers(log_widget):
    log_widget.insert(tk.END, "Blocking ads and trackers...\n")
    hosts_url = "https://someonewhocares.org/hosts/hosts"
    response = requests.get(hosts_url)
    with open("C:\\Windows\\System32\\drivers\\etc\\hosts", "a") as hosts_file:
        hosts_file.write(response.text)
    log_widget.insert(tk.END, "Finished updating hosts file to block ads and trackers.\n")

def enable_firewall(log_widget):
    log_widget.insert(tk.END, "Enabling Windows Firewall...\n")
    subprocess.run(["netsh", "advfirewall", "set", "allprofiles", "state", "on"])
    log_widget.insert(tk.END, "Windows Firewall enabled.\n")

def change_dns(log_widget):
    log_widget.insert(tk.END, "Changing DNS to Mullvad...\n")
    dns_servers = ["100.64.0.1", "100.64.0.2"]
    for dns in dns_servers:
        subprocess.run(["netsh", "interface", "ipv4", "set", "dnsservers", "name=\"Wi-Fi\"", "source=static", f"address={dns}", "validate=no"])
    log_widget.insert(tk.END, "DNS changed to Mullvad DNS.\n")

def disk_cleanup(log_widget):
    log_widget.insert(tk.END, "Performing disk cleanup...\n")
    subprocess.run(["cleanmgr", "/sagerun:1"])
    log_widget.insert(tk.END, "Disk cleanup completed.\n")

def apply_all_privacy_features(log_widget):
    log_widget.insert(tk.END, "Applying all privacy features...\n")
    url = "https://raw.githubusercontent.com/braydos-h/Anti-Spyware/main/firewall%20settings.txt"
    ips_to_block = download_ips(url)
    block_ips_with_firewall(ips_to_block, log_widget)
    modify_privacy_settings(log_widget)
    clear_browser_data(log_widget)
    disable_unnecessary_services(log_widget)
    block_ads_and_trackers(log_widget)
    enable_firewall(log_widget)
    change_dns(log_widget)
    disk_cleanup(log_widget)
    messagebox.showinfo("Privacy Enhancer", "All privacy features applied successfully!")

def check_mullvad_vpn():
    try:
        response = requests.get("https://am.i.mullvad.net/json")
        data = response.json()
        return data["mullvad_exit_ip"], data["ip"], data["country"]
    except Exception as e:
        return None, None, None

def update_status_bar(status_label):
    is_connected, ip, country = check_mullvad_vpn()
    status = f"IP: {ip}, Country: {country}, Mullvad: {'Connected' if is_connected else 'Not Connected'}"
    status_label.config(text=status)

def main():
    if not is_admin():
        print("This script must be run as an administrator.")
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
        return

    root = tk.Tk()
    root.title("Privacy Enhancer")
    root.geometry("500x700")
    root.configure(bg="#2d2d2d")

    tk.Label(root, text="Privacy Enhancer", font=("Helvetica", 16), bg="#2d2d2d", fg="#ffffff").pack(pady=10)

    log_widget = scrolledtext.ScrolledText(root, width=60, height=15, bg="#1e1e1e", fg="#00ff00")
    log_widget.pack(pady=10)

    button_frame = tk.Frame(root, bg="#2d2d2d")
    button_frame.pack(pady=10)

    tk.Button(button_frame, text="Block Telemetry IPs", command=lambda: block_ips_with_firewall(download_ips("https://raw.githubusercontent.com/braydos-h/Anti-Spyware/main/firewall%20settings.txt"), log_widget), bg="#4CAF50", fg="#ffffff").pack(pady=5)
    tk.Button(button_frame, text="Disable Cortana & Telemetry", command=lambda: modify_privacy_settings(log_widget), bg="#2196F3", fg="#ffffff").pack(pady=5)
    tk.Button(button_frame, text="Clear Browser Data", command=lambda: clear_browser_data(log_widget), bg="#f44336", fg="#ffffff").pack(pady=5)
    tk.Button(button_frame, text="Disable Unnecessary Services", command=lambda: disable_unnecessary_services(log_widget), bg="#ff9800", fg="#ffffff").pack(pady=5)
    tk.Button(button_frame, text="Block Ads & Trackers", command=lambda: block_ads_and_trackers(log_widget), bg="#9C27B0", fg="#ffffff").pack(pady=5)
    tk.Button(button_frame, text="Enable Firewall", command=lambda: enable_firewall(log_widget), bg="#3F51B5", fg="#ffffff").pack(pady=5)
    tk.Button(button_frame, text="Change DNS to Mullvad", command=lambda: change_dns(log_widget), bg="#00BCD4", fg="#ffffff").pack(pady=5)
    tk.Button(button_frame, text="Disk Cleanup", command=lambda: disk_cleanup(log_widget), bg="#8BC34A", fg="#ffffff").pack(pady=5)
    tk.Button(button_frame, text="Apply All Privacy Features", command=lambda: apply_all_privacy_features(log_widget), bg="#FF5722", fg="#ffffff").pack(pady=5)

    tk.Label(root, text="Beta 0.1 by Braydos", font=("Helvetica", 10), bg="#2d2d2d", fg="#ffffff").pack(side=tk.LEFT, padx=10)

    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    tk.Label(root, text=current_time, font=("Helvetica", 10), bg="#2d2d2d", fg="#ffffff").pack(side=tk.RIGHT, padx=10)

    status_label = tk.Label(root, text="", font=("Helvetica", 10), bg="#2d2d2d", fg="#ffffff")
    status_label.pack(side=tk.BOTTOM, fill=tk.X)

    def show_privacy_info():
        messagebox.showinfo("Privacy Features", "1. Block Telemetry IPs\n2. Disable Cortana & Telemetry\n3. Clear Browser Data\n4. Disable Unnecessary Services\n5. Block Ads & Trackers\n6. Enable Firewall\n7. Change DNS to Mullvad\n8. Disk Cleanup\n9. Apply All Privacy Features")

    menu_bar = tk.Menu(root)
    help_menu = tk.Menu(menu_bar, tearoff=0)
    help_menu.add_command(label="Privacy Features", command=show_privacy_info)
    menu_bar.add_cascade(label="Help", menu=help_menu)
    root.config(menu=menu_bar)

    update_status_bar(status_label)

    root.mainloop()

if __name__ == "__main__":
    main()
