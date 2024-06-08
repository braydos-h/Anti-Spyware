import customtkinter as ctk
import subprocess
import requests
import ctypes
import sys
import datetime
import json

# Check for admin privileges
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

# Download IPs from a URL
def download_ips(url):
    response = requests.get(url)
    response.raise_for_status()
    ips = response.text.splitlines()
    return [ip for ip in ips if ip and not ip.startswith("#")]

# Block IPs using firewall
def block_ips_with_firewall(ips, log_widget):
    actions = []
    for ip in ips:
        log_widget.insert(ctk.END, f"Blocking IP: {ip}\n")
        log_widget.see(ctk.END)
        log_widget.update()
        subprocess.run(["netsh", "advfirewall", "firewall", "add", "rule", f"name=Block {ip}", "dir=out", "action=block", f"remoteip={ip}"])
        actions.append(f"Blocked IP: {ip}")
    log_widget.insert(ctk.END, "Finished blocking IP addresses.\n")
    return actions

# Modify privacy settings
def modify_privacy_settings(log_widget):
    actions = []
    log_widget.insert(ctk.END, "Disabling Cortana...\n")
    subprocess.run(["reg", "add", "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\Windows Search", "/v", "AllowCortana", "/t", "REG_DWORD", "/d", "0", "/f"])
    actions.append("Disabled Cortana")
    log_widget.insert(ctk.END, "Disabling telemetry...\n")
    subprocess.run(["reg", "add", "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\DataCollection", "/v", "AllowTelemetry", "/t", "REG_DWORD", "/d", "0", "/f"])
    actions.append("Disabled telemetry")
    log_widget.insert(ctk.END, "Finished modifying privacy settings.\n")
    return actions

# Clear browser data
def clear_browser_data(log_widget):
    actions = []
    browsers = ["chrome", "firefox", "edge"]
    for browser in browsers:
        log_widget.insert(ctk.END, f"Clearing {browser} data...\n")
        subprocess.run([browser, "--clear-browsing-data=all"])
        actions.append(f"Cleared {browser} data")
    log_widget.insert(ctk.END, "Finished clearing browser data.\n")
    return actions

# Disable unnecessary services
def disable_unnecessary_services(log_widget):
    actions = []
    services = ["DiagTrack", "dmwappushservice"]
    for service in services:
        log_widget.insert(ctk.END, f"Disabling service: {service}\n")
        subprocess.run(["sc", "config", service, "start=", "disabled"])
        actions.append(f"Disabled service: {service}")
    log_widget.insert(ctk.END, "Finished disabling services.\n")
    return actions

# Block ads and trackers
def block_ads_and_trackers(log_widget):
    hosts_url = "https://someonewhocares.org/hosts/hosts"
    response = requests.get(hosts_url)
    with open("C:\\Windows\\System32\\drivers\\etc\\hosts", "a") as hosts_file:
        hosts_file.write(response.text)
    log_widget.insert(ctk.END, "Finished updating hosts file to block ads and trackers.\n")

# Enable firewall
def enable_firewall(log_widget):
    log_widget.insert(ctk.END, "Enabling Windows Firewall...\n")
    subprocess.run(["netsh", "advfirewall", "set", "allprofiles", "state", "on"])
    log_widget.insert(ctk.END, "Windows Firewall enabled.\n")

# Change DNS to Mullvad
def change_dns(log_widget):
    log_widget.insert(ctk.END, "Changing DNS to Mullvad...\n")
    dns_servers = ["100.64.0.1", "100.64.0.2"]
    for dns in dns_servers:
        subprocess.run(["netsh", "interface", "ipv4", "set", "dnsservers", "name=\"Wi-Fi\"", "source=static", f"address={dns}", "validate=no"])
    log_widget.insert(ctk.END, "DNS changed to Mullvad DNS.\n")

# Perform disk cleanup
def disk_cleanup(log_widget):
    log_widget.insert(ctk.END, "Performing disk cleanup...\n")
    subprocess.run(["cleanmgr", "/sagerun:1"])
    log_widget.insert(ctk.END, "Disk cleanup completed.\n")

# Apply all privacy features
def apply_all_privacy_features(log_widget):
    log_widget.insert(ctk.END, "Applying all privacy features...\n")
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
    ctk.messagebox.show_info("Privacy Enhancer", "All privacy features applied successfully!")

# Create the main GUI
def create_gui():
    app = ctk.CTk()
    app.title("Privacy Enhancer")
    app.geometry("800x1000")
    ctk.set_appearance_mode("system")  # Use system appearance
    ctk.set_default_color_theme("dark-blue")  # Set a theme

    # Title
    title_label = ctk.CTkLabel(app, text="Anti Spy Ware by Braydos-h", font=("Helvetica", 16))
    title_label.pack(pady=10)

    # Log widget
    log_widget = ctk.CTkTextbox(app, width=750, height=400)
    log_widget.pack(pady=10)

    # Button frame
    button_frame = ctk.CTkFrame(app)
    button_frame.pack(pady=10, fill="x", expand=True)

    # Create buttons
    buttons = [
        ("Block Telemetry IPs", lambda: block_ips_with_firewall(download_ips("https://raw.githubusercontent.com/braydos-h/Anti-Spyware/main/firewall%20settings.txt"), log_widget)),
        ("Disable Cortana & Telemetry", lambda: modify_privacy_settings(log_widget)),
        ("Clear Browser Data", lambda: clear_browser_data(log_widget)),
        ("Disable Unnecessary Services", lambda: disable_unnecessary_services(log_widget)),
        ("Block Ads & Trackers", lambda: block_ads_and_trackers(log_widget)),
        ("Enable Firewall", lambda: enable_firewall(log_widget)),
        ("Change DNS to Mullvad", lambda: change_dns(log_widget)),
        ("Disk Cleanup", lambda: disk_cleanup(log_widget)),
        ("Apply All Privacy Features", lambda: apply_all_privacy_features(log_widget))
    ]

    for text, command in buttons:
        button = ctk.CTkButton(button_frame, text=text, command=command)
        button.pack(pady=5, padx=10, fill="x")

    # Status bar
    status_label = ctk.CTkLabel(app, text="Beta 0.2.5 by Braydos", font=("Helvetica", 10))
    status_label.pack(side="left", padx=10)

    # Time display
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    time_label = ctk.CTkLabel(app, text=current_time, font=("Helvetica", 10))
    time_label.pack(side="right", padx=10)

    # Run the application
    app.mainloop()

# Check for admin privileges and run the GUI
if is_admin():
    create_gui()
else:
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
