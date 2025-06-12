import requests
import json
import time
from datetime import datetime
from collections import Counter

# ONOS API Ayarları
ONOS_IP = "127.0.0.1"
ONOS_PORT = "8181"
ONOS_AUTH = ("onos", "rocks")

# Snapshot kayıt dosyası
SNAPSHOT_FILE = "full_network_snapshot.json"

# 🔧 ONOS cihazlarını al
def get_onos_devices():
    url = f"http://{ONOS_IP}:{ONOS_PORT}/onos/v1/devices"
    r = requests.get(url, auth=ONOS_AUTH)
    return r.json().get("devices", [])

# 🔧 ONOS bağlantı (link) bilgilerini al
def get_onos_links():
    url = f"http://{ONOS_IP}:{ONOS_PORT}/onos/v1/links"
    r = requests.get(url, auth=ONOS_AUTH)
    return r.json().get("links", [])

# 🔧 Flow sayılarını her cihaz için al
def get_onos_flow_stats():
    url = f"http://{ONOS_IP}:{ONOS_PORT}/onos/v1/flows"
    r = requests.get(url, auth=ONOS_AUTH)
    flows = r.json().get("flows", [])
    flow_count_per_device = Counter()
    for flow in flows:
        flow_count_per_device[flow['deviceId']] += 1
    return flow_count_per_device

# 🔧 Port istatistiklerini al
def get_onos_port_stats():
    url = f"http://{ONOS_IP}:{ONOS_PORT}/onos/v1/statistics/ports"
    r = requests.get(url, auth=ONOS_AUTH)
    port_stats = r.json().get("statistics", [])

    bytes_per_device = Counter()
    packets_per_device = Counter()
    avg_packet_size_per_device = {}

    for device_entry in port_stats:
        dev = device_entry['device']
        total_bytes = 0
        total_packets = 0
        for port_stat in device_entry.get("ports", []):
            total_bytes += port_stat.get('bytesReceived', 0) + port_stat.get('bytesSent', 0)
            total_packets += port_stat.get('packetsReceived', 0) + port_stat.get('packetsSent', 0)
        bytes_per_device[dev] = total_bytes
        packets_per_device[dev] = total_packets
        avg_packet_size_per_device[dev] = (total_bytes / total_packets) if total_packets > 0 else 0

    return bytes_per_device, packets_per_device, avg_packet_size_per_device

# 🔄 Anlık snapshot verisi topla
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
        if not device.get("available"):
            continue  # Sadece aktif cihazlar

        device_id = device.get('id')
        annotations = device.get('annotations', {})

        snapshot = {
            "timestamp": timestamp,
            "id": device_id,
            "type": device.get('type'),
            "available": device.get('available'),
            "protocol": device.get('protocol', 'unknown'),
            "mfr": device.get('mfr', 'unknown'),
            "sw_version": device.get('sw', 'unknown'),
            "hw_version": device.get('hw', 'unknown'),
            "mgmt_address": annotations.get('managementAddress', 'unknown'),
            "flow_count": flow_counts.get(device_id, 0),
            "total_packets": packets_counts.get(device_id, 0),
            "total_bytes": bytes_counts.get(device_id, 0),
            "avg_packet_size": avg_packet_sizes.get(device_id, 0),
            "link_count": degrees.get(device_id, 0)
        }
        snapshots.append(snapshot)

    # JSONL olarak dosyaya yaz
    with open(SNAPSHOT_FILE, "a") as f:
        for entry in snapshots:
            f.write(json.dumps(entry) + "\n")

    print(f"[{timestamp}] ✅ Snapshot collected: {len(snapshots)} entries")

# 🌀 Sonsuz döngü: her 5 saniyede bir snapshot al
if __name__ == "__main__":
    while True:
        try:
            collect_snapshot()
            time.sleep(5)
        except Exception as e:
            print(f"❌ Hata: {e}")
            time.sleep(5)

