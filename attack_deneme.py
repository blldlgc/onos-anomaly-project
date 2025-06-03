import time
import os

def get_mininet_pid():
    try:
        pid = os.popen("ps aux | grep 'sudo mn' | grep -v grep | awk '{print $2}'").read().strip()
        if pid:
            return pid
        else:
            raise Exception("Mininet PID bulunamadı. Mininet çalışıyor mu?")
    except Exception as e:
        print(f"Hata: {e}")
        return None

def send_command(command):
    pid = get_mininet_pid()
    if pid:
        full_cmd = f'sudo mnexec -a {pid} {command}'
        os.system(full_cmd)
    else:
        print("Mininet PID bulunamadığı için komut gönderilemedi.")

def link_down_up():
    print("[Link Down] s1 <-> s2")
    send_command('mnexec link s1 s2 down')
    time.sleep(20)
    print("[Link Up] s1 <-> s2")
    send_command('mnexec link s1 s2 up')

def stop_start_switch():
    print("[Switch Down] s3")
    send_command('mnexec stop s3')
    time.sleep(20)
    print("[Switch Up] s3")
    send_command('mnexec start s3')

def heavy_traffic():
    print("[Heavy Traffic] iperf spam from 10 hosts")
    for i in range(1, 11):
        send_command(f'xterm h{i} -e "iperf -c 10.0.0.2 -t 30 &"')
    time.sleep(30)
    print("[Heavy Traffic Ended]")

def rtt_increase():
    print("[RTT Increase] s1-eth1 netem delay + loss")
    send_command('tc qdisc add dev s1-eth1 root netem delay 300ms loss 20%')
    time.sleep(20)
    print("[RTT Normalize]")
    send_command('tc qdisc del dev s1-eth1 root netem')

def run_attack_sequence():
    while True:
        print("=== Anomaly Attack Sequence Start ===")
        link_down_up()
        time.sleep(10)
        stop_start_switch()
        time.sleep(10)
        heavy_traffic()
        time.sleep(10)
        rtt_increase()
        print("=== Sequence Complete. Waiting 60 seconds before next ===")
        time.sleep(60)

if __name__ == "__main__":
    run_attack_sequence()

