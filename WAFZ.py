#code By wafa | telegram:har_ut | Grop Telegram:https://t.me/ar_pm

import psutil
import subprocess
import time
import os
#################
BLOCKED_PORTS_FILE = "Ports_Blocked.txt"

os.system("clear")
print("""\033[0;32m
                    ██╗    ██╗ █████╗ ███████╗███████╗
                    ██║    ██║██╔══██╗██╔════╝╚══███╔╝
                    ██║ █╗ ██║███████║█████╗    ███╔╝
                    ██║███╗██║██╔══██║██╔══╝   ███╔╝
                    ╚███╔███╔╝██║  ██║██║     ███████╗
                     ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝     ╚══════╝
                    \033[0;37m[\033[0;33mV\033[0;32m1.1\033[0;37m] \033[0;37m- \033[0;37m[\033[0;33mTelegram \033[0;37m: \033[0;32mHar_ut\033[0;37m]
                    \033[0;37m""")

def is_system_port(port):
    return port < 1024
def get_open_ports():
    return [conn.laddr.port for conn in psutil.net_connections()]
def block_port(port):
    subprocess.run(['sudo', 'iptables', '-A', 'INPUT', '-p', 'tcp', '--dport', str(port), '-j', 'DROP'])
    current_time = os.popen('date +"%Y/%m/%d - %H:%M:%S"').read().strip()
    print(f"[!] \033[0;33mPort \033[0;37m[\033[0;36m{port}\033[0;37m]\033[0;37m has been \033[0;37m[\033[0;31mBlocked!\033[0;37m]" + " - " + "[\033[0;33m" + current_time + "\033[0;37m]")
def load_blocked_ports():
    blocked_ports = set()
    if os.path.exists(BLOCKED_PORTS_FILE):
        with open(BLOCKED_PORTS_FILE, "r") as blocked_ports_file:
            blocked_ports = set(map(int, blocked_ports_file.read().split()))
    return blocked_ports
def save_blocked_ports(blocked_ports):
    with open(BLOCKED_PORTS_FILE, "w") as blocked_ports_file:
        blocked_ports_file.write("\n".join(map(str, blocked_ports)))
def monitor_network_changes():
    blocked_ports = load_blocked_ports()
    while True:
        time.sleep(1)
        current_ports = set(get_open_ports())
        current_time = os.popen('date +"%Y/%m/%d - %H:%M:%S"').read().strip()

        new_ports = current_ports - blocked_ports
        if new_ports:
            for port in new_ports:
                if not is_system_port(port):
                    print(f"[+] \033[0;32mNew Port OPEIND\033[0;37m: \033[0;36m{port} \033[0;37m[\033[0;31mBlocking!\033[0;37m]" + " - " + "[\033[0;33m" + current_time + "\033[0;37m]")
                    block_port(port)
                    blocked_ports.add(port)
        manual_blocked_ports = load_blocked_ports()
        for port in manual_blocked_ports:
            if port not in blocked_ports:
                print(f"[~] Manual Block: \033[0;32mPort \033[0;37m[\033[0;36m{port}\033[0;37m] \033[0;37m[\033[0;31mBlocking!\033[0;37m] - [\033[0;33m{current_time}\033[0;37m]")
                block_port(port)
                blocked_ports.add(port)

        save_blocked_ports(blocked_ports)

if __name__ == "__main__":
    monitor_network_changes()

