import psutil
import subprocess
import time
import os

os.system("clear")
print("""\033[0;32m
                    ██╗    ██╗ █████╗ ███████╗███████╗
                    ██║    ██║██╔══██╗██╔════╝╚══███╔╝
                    ██║ █╗ ██║███████║█████╗    ███╔╝
                    ██║███╗██║██╔══██║██╔══╝   ███╔╝
                    ╚███╔███╔╝██║  ██║██║     ███████╗
                     ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝     ╚══════╝
                    \033[0;37m[\033[0;33mV\033[0;32m1.0\033[0;37m] \033[0;37m- \033[0;37m[\033[0;33mTelegram \033[0;37m: \033[0;32mHar_ut\033[0;37m]

\033[0;37m""")
def is_system_port(port):
    return port < 1024

def get_open_ports():
    return [conn.laddr.port for conn in psutil.net_connections()]

def block_port(port):
    subprocess.run(['sudo', 'iptables', '-A', 'INPUT', '-p', 'tcp', '--dport', str(port), '-j', 'DROP'])
    current_time = os.popen('date +"%Y/%m/%d - %H:%M:%S"').read().strip()
    print(f"[!] \033[0;33mPort \033[0;37m[\033[0;36m{port}\033[0;37m]\033[0;37m has been \033[0;37m[\033[0;31mBlocked!\033[0;37m]"+ " - " + "[\033[0;33m" + current_time + "\033[0;37m]")

def monitor_network_changes():
    previous_ports = set(get_open_ports())

    while True:
        time.sleep(1)
        current_ports = set(get_open_ports())
        current_time = os.popen('date +"%Y/%m/%d - %H:%M:%S"').read().strip()

        new_ports = current_ports - previous_ports
        if new_ports:
            for port in new_ports:
                if not is_system_port(port):
                    print(f"[+] \033[0;32mNew Port OPEIND\033[0;37m: \033[0;36m{port} \033[0;37m[\033[0;31mBlocking!\033[0;37m]" + " - " + "[\033[0;33m" + current_time + "\033[0;37m]")
                    block_port(port)

        closed_ports = previous_ports - current_ports
        if closed_ports:
            print(f"[-] Ports Closed: \033[0;37m[\033[0;31m{', '.join(map(str, closed_ports))}\033[0;37m]" + " - " + "[\033[0;33m" + current_time + "\033[0;37m]")

        previous_ports = current_ports

if __name__ == "__main__":
    monitor_network_changes()
