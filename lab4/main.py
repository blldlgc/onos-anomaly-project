from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
import joblib
import numpy as np

# ONOS API Ayarları
ONOS_IP = "localhost"
ONOS_PORT = 8181
AUTH = ('onos', 'rocks')

# ML Model Yolu
MODEL_PATH = "model/anomaly_detector.pkl"

# Modeli yükle
try:
    model = joblib.load(MODEL_PATH)
except Exception as e:
    print(f"Model yüklenemedi: {e}")
    model = None

# FastAPI uygulaması
app = FastAPI(
    title="SDN Anomaly Detection API",
    description="ONOS'tan cihaz, flow ve link verilerini çeken ve anomaly tahmini yapan API",
    version="1.0"
)

# CORS Ayarı (React ile iletişim için)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/devices")
def get_devices():
    # ONOS'tan cihaz verilerini çek
    device_url = f"http://{ONOS_IP}:{ONOS_PORT}/onos/v1/devices"
    device_resp = requests.get(device_url, auth=AUTH)
    if device_resp.status_code != 200:
        return {"error": f"ONOS devices API hatası: {device_resp.status_code}"}

    devices_raw = device_resp.json().get('devices', [])
    devices = {d['id']: {"id": d['id'], "flow_count": 0, "total_packets": 0, "total_bytes": 0, "avg_packet_size": 0, "link_count": 0} for d in devices_raw}

    # Flow verilerini çek ve cihazlara ekle
    flow_url = f"http://{ONOS_IP}:{ONOS_PORT}/onos/v1/flows"
    flow_resp = requests.get(flow_url, auth=AUTH)
    if flow_resp.status_code == 200:
        for f in flow_resp.json().get('flows', []):
            device_id = f.get('deviceId')
            if device_id in devices:
                devices[device_id]['flow_count'] += 1
                devices[device_id]['total_packets'] += f.get('packets', 0)
                devices[device_id]['total_bytes'] += f.get('bytes', 0)

    # Ortalama paket boyutunu hesapla
    for d in devices.values():
        if d['flow_count'] > 0:
            d['avg_packet_size'] = d['total_bytes'] / d['flow_count']

    # Link verilerini çek ve cihazlara ekle
    link_url = f"http://{ONOS_IP}:{ONOS_PORT}/onos/v1/links"
    link_resp = requests.get(link_url, auth=AUTH)
    if link_resp.status_code == 200:
        for l in link_resp.json().get('links', []):
            src = l.get('src', {}).get('device')
            dst = l.get('dst', {}).get('device')
            if src in devices:
                devices[src]['link_count'] += 1
            if dst in devices:
                devices[dst]['link_count'] += 1

    return list(devices.values())

@app.post("/predict/{device_id}")
def predict_anomaly(device_id: str):
    # Cihaz verilerini ONOS'tan çek
    device_url = f"http://{ONOS_IP}:{ONOS_PORT}/onos/v1/devices/{device_id}"
    device_resp = requests.get(device_url, auth=AUTH)
    if device_resp.status_code != 200:
        return {"error": f"ONOS device API hatası: {device_resp.status_code}"}

    # Flow ve link bilgilerini de çekelim
    flow_url = f"http://{ONOS_IP}:{ONOS_PORT}/onos/v1/flows/{device_id}"
    flow_resp = requests.get(flow_url, auth=AUTH)

    link_url = f"http://{ONOS_IP}:{ONOS_PORT}/onos/v1/links"
    link_resp = requests.get(link_url, auth=AUTH)

    # Verileri hesapla
    flow_count = 0
    total_packets = 0
    total_bytes = 0
    avg_packet_size = 0
    link_count = 0

    if flow_resp.status_code == 200:
        flows = flow_resp.json().get('flows', [])
        flow_count = len(flows)
        for f in flows:
            total_packets += f.get('packets', 0)
            total_bytes += f.get('bytes', 0)
        avg_packet_size = total_bytes / flow_count if flow_count > 0 else 0

    if link_resp.status_code == 200:
        for l in link_resp.json().get('links', []):
            if device_id in (l.get('src', {}).get('device'), l.get('dst', {}).get('device')):
                link_count += 1

    # Anomaly tahmini yap
    if model is None:
        return {"error": "Model yüklenemedi."}

    data = np.array([[flow_count, total_packets, total_bytes, avg_packet_size, link_count]])
    prediction = model.predict(data)

    return {
        "device_id": device_id,
        "flow_count": flow_count,
        "total_packets": total_packets,
        "total_bytes": total_bytes,
        "avg_packet_size": avg_packet_size,
        "link_count": link_count,
        "anomaly": int(prediction[0])
    }

