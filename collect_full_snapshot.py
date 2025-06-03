import requests
import os
import json
import time
from datetime import datetime
from collections import Counter

# ONOS API Ayarları
ONOS_IP = "127.0.0.1"
ONOS_PORT = "8181"
ONOS_AUTH = ("onos", "rocks")

# Mininet Host Listesi (örnek)
hosts = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'h8', 'h9', 'h10',
         'h11', 'h12', 'h13', 'h14', 'h15', 'h16', 'h17', 'h18', 'h19', 'h20',
         'h21', 'h22', 'h23', 'h24', 'h25', 'h26', 'h27', 'h28', 'h29', 'h30',
         'h31', 'h32', 'h33', 'h34', 'h35', 'h36', 'h37', 'h38', 'h39', 'h40',
         'h41', 'h42', 'h43', 'h44', 'h45', 'h46', 'h47', 'h48', 'h49', 'h50',
         'h51', 'h52', 'h53', 'h54', 'h55', 'h56', 'h57', 'h58', 'h59', 'h60']


# Snapshot JSON Dosyası
SNAPSHOT_FILE = "full_network_snapshot.json"

def get_onos_devices():
    url = f"http://{ONOS_IP}:{ONOS_PORT}/onos/v1/devices"
    r = requests.get(url, auth=ONOS_AUTH)
    return r.json().get("devices", [])

def get_onos_links():
    url = f"http://{ONOS_IP}:{ONOS_PORT}/onos/v1/links"
    r = requests.get(url, auth=ONOS_AUTH)
    return r.json().get("links", [])

def get_onos_flow_stats():
    url = f"http://{ONOS_IP}:{ONOS_PORT}/onos/v1/flows"
    r = requests.get(url, auth=ONOS_AUTH)
    flows = r.json().get("flows", [])
    flow_count_per_device = Counter()
    for flow in flows:
        flow_count_per_device[flow['deviceId']] += 1
    return flow_count_per_device

def get_onos_port_stats():
    url = f"http://{ONOS_IP}:{ONOS_PORT}/onos/v1/statistics/ports"
    r = requests.get(url, auth=ONOS_AUTH)
    port_stats = r.json().get("statistics", [])
    stats_per_device = Counter()
    bytes_per_device = Counter()
    packets_per_device = Counter()
    avg_packet_size_per_device = {}
    for stat in port_stats:
        dev = stat['device']
        bytes_count = stat.get('bytes', 0)
        packets_count = stat.get('packets', 0)
        stats_per_device[dev] += 1
        bytes_per_device[dev] += bytes_count
        packets_per_device[dev] += packets_count
        avg_packet_size_per_device[dev] = (bytes_count / packets_count) if packets_count > 0 else 0
    return bytes_per_device, packets_per_device, avg_packet_size_per_device

def collect_snapshot():
    timestamp = datetime.now().isoformat()
    devices = get_onos_devices()
    links = get_onos_links()
    flow_counts = get_onos_flow_stats()
    bytes_counts, packets_counts, avg_packet_sizes = get_onos_port_stats()
    
    # Graph metric: link_count (degree)
    degrees = Counter()
    for link in links:
        degrees[link['src']['device']] += 1
        degrees[link['dst']['device']] += 1

    snapshots = []
    for device in devices:
        device_id = device.get('id')
        snapshot = {
            "timestamp": timestamp,
            "id": device_id,
            "type": device.get('type'),
            "available": device.get('available'),
            "protocol": device.get('protocols', [None])[0],
            "flow_count": flow_counts.get(device_id, 0),
            "total_packets": packets_counts.get(device_id, 0),
            "total_bytes": bytes_counts.get(device_id, 0),
            "avg_packet_size": avg_packet_sizes.get(device_id, 0),
            "link_count": degrees.get(device_id, 0)
        }
        snapshots.append(snapshot)

    # JSONL formatında kaydet
    with open(SNAPSHOT_FILE, "a") as f:
        for entry in snapshots:
            f.write(json.dumps(entry) + "\n")

    print(f"[{timestamp}] Snapshot collected: {len(snapshots)} entries")

# Ana döngü
if __name__ == "__main__":
    while True:
        try:
            collect_snapshot()
            time.sleep(5)
        except Exception as e:
            print(f"Hata: {e}")
            time.sleep(5)

