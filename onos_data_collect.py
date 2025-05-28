import requests
import pandas as pd

# ONOS API bilgileri
ONOS_IP = "localhost"  # veya IP adresi
ONOS_PORT = 8181
AUTH = ('onos', 'rocks')

# API URL'leri
DEVICE_URL = f"http://{ONOS_IP}:{ONOS_PORT}/onos/v1/devices"
LINK_URL = f"http://{ONOS_IP}:{ONOS_PORT}/onos/v1/links"
FLOW_URL = f"http://{ONOS_IP}:{ONOS_PORT}/onos/v1/flows"

# Veri çekme fonksiyonları
def get_data(url):
    response = requests.get(url, auth=AUTH)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Hata: {response.status_code}")
        return None

# Cihaz verilerini çek ve CSV'ye yaz
device_data = get_data(DEVICE_URL)
if device_data:
    devices = []
    for d in device_data['devices']:
        devices.append({
            'id': d.get('id'),
            'type': d.get('type'),
            'available': d.get('available'),
            'mfr': d.get('mfr'),
            'hw': d.get('hw'),
            'sw': d.get('sw'),
            'protocol': d.get('protocol'),
        })
    df_devices = pd.DataFrame(devices)
    df_devices.to_csv('onos_devices.csv', index=False)
    print("Cihaz verileri onos_devices.csv'ye kaydedildi.")

# Bağlantı (Link) verilerini çek ve CSV'ye yaz
link_data = get_data(LINK_URL)
if link_data:
    links = []
    for l in link_data['links']:
        links.append({
            'src': l['src']['device'],
            'src_port': l['src']['port'],
            'dst': l['dst']['device'],
            'dst_port': l['dst']['port'],
            'type': l.get('type'),
            'state': l.get('state')
        })
    df_links = pd.DataFrame(links)
    df_links.to_csv('onos_links.csv', index=False)
    print("Bağlantı verileri onos_links.csv'ye kaydedildi.")

# Akış (Flow) verilerini çek ve CSV'ye yaz
flow_data = get_data(FLOW_URL)
if flow_data:
    flows = []
    for entry in flow_data['flows']:
        flows.append({
            'deviceId': entry.get('deviceId'),
            'flowId': entry.get('id'),
            'state': entry.get('state'),
            'priority': entry.get('priority'),
            'tableId': entry.get('tableId'),
            'isPermanent': entry.get('isPermanent'),
            'packets': entry.get('packets'),
            'bytes': entry.get('bytes'),
        })
    df_flows = pd.DataFrame(flows)
    df_flows.to_csv('onos_flows.csv', index=False)
    print("Akış verileri onos_flows.csv'ye kaydedildi.")
