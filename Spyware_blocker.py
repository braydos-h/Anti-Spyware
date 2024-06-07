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
    browsers = ["chrome", "firefox", "edge"]
    for browser in browsers:
        log_widget.insert(tk.END, f"Clearing {browser} data...\n")
        subprocess.run([browser, "--clear-browsing-data=all"])
    log_widget.insert(tk.END, "Finished clearing browser data.\n")

def disable_unnecessary_services(log_widget):
    services = ["DiagTrack", "dmwappushservice"]
    for service in services:
        log_widget.insert(tk.END, f"Disabling service: {service}\n")
        subprocess.run(["sc", "config", service, "start=", "disabled"])
    log_widget.insert(tk.END, "Finished disabling unnecessary services.\n")

def block_ads_and_trackers(log_widget):
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

def toggle_dark_mode():
    global dark_mode
    dark_mode = not dark_mode
    if dark_mode:
        root.configure(bg="#1e1e1e")
        log_widget.configure(bg="#1e1e1e", fg="#ffffff")
        button_frame.configure(bg="#1e1e1e")
        status_label.configure(bg="#1e1e1e", fg="#ffffff")
    else:
        root.configure(bg="#2d2d2d")
        log_widget.configure(bg="#1e1e1e", fg="#00ff00")
        button_frame.configure(bg="#2d2d2d")
        status_label.configure(bg="#2d2d2d", fg="#ffffff")

def main():
    global root, log_widget, button_frame, status_label, dark_mode
    dark_mode = False

    if not is_admin():
        print("This script must be run as an administrator.")
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
        return

    root = tk.Tk()
    root.title("Privacy Enhancer")
    root.geometry("600x800")
    root.configure(bg="#2d2d2d")

    tk.Label(root, text="Privacy Enhancer", font=("Helvetica", 16), bg="#2d2d2d", fg="#ffffff").pack(pady=10)

    log_widget = scrolledtext.ScrolledText(root, width=80, height=20, bg="#1e1e1e", fg="#00ff00")
    log_widget.pack(pady=10)

    button_frame = tk.Frame(root, bg="#2d2d2d")
    button_frame.pack(pady=10)

    buttons = [
        ("Block Telemetry IPs", "#4CAF50", lambda: block_ips_with_firewall(download_ips("https://raw.githubusercontent.com/braydos-h/Anti-Spyware/main/firewall%20settings.txt"), log_widget)),
        ("Disable Cortana & Telemetry", "#2196F3", lambda: modify_privacy_settings(log_widget)),
        ("Clear Browser Data", "#f44336", lambda: clear_browser_data(log_widget)),
        ("Disable Unnecessary Services", "#ff9800", lambda: disable_unnecessary_services(log_widget)),
        ("Block Ads & Trackers", "#9C27B0", lambda: block_ads_and_trackers(log_widget)),
        ("Enable Firewall", "#3F51B5", lambda: enable_firewall(log_widget)),
        ("Change DNS to Mullvad", "#00BCD4", lambda: change_dns(log_widget)),
        ("Disk Cleanup", "#8BC34A", lambda: disk_cleanup(log_widget)),
        ("Apply All Privacy Features", "#FF5722", lambda: apply_all_privacy_features(log_widget))
    ]

    for text, color, command in buttons:
        tk.Button(button_frame, text=text, command=command, bg=color, fg="#ffffff").pack(pady=5)

    tk.Button(root, text="Toggle Dark Mode", command=toggle_dark_mode, bg="#777777", fg="#ffffff").pack(pady=5)

    tk.Label(root, text="Beta 0.2 by Braydos", font=("Helvetica", 10), bg="#2d2d2d", fg="#ffffff").pack(side=tk.LEFT, padx=10)

    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    tk.Label(root, text=current_time, font=("Helvetica", 10), bg="#2d2d2d", fg="#ffffff").pack(side=tk.RIGHT, padx=10)

    status_label = tk.Label(root, text="", font=("Helvetica", 10), bg="#2d2d2d", fg="#ffffff")
    status_label.pack(side=tk.BOTTOM, fill=tk.X)

    update_status_bar(status_label)

    root.mainloop()

if __name__ == "__main__":
    main()
