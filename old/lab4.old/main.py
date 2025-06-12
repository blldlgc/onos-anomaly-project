from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
import numpy as np
from tensorflow.keras.models import load_model
import joblib

# === ONOS API Ayarları ===
ONOS_IP = "localhost"
ONOS_PORT = 8181
AUTH = ('onos', 'rocks')

# === Model ve Scaler Yolu ===
MODEL_PATH = "model/packet_predictor_model.h5"
SCALER_PATH = "model/scaler.pkl"

# === Model ve Scaler Yükleme ===
try:
    model = load_model(MODEL_PATH, compile=False)
    scaler = joblib.load(SCALER_PATH)
    print("✅ Model ve scaler başarıyla yüklendi.")
except Exception as e:
    print(f"❌ Model veya scaler yüklenemedi: {e}")
    model = None
    scaler = None

# === FastAPI Uygulaması ===
app = FastAPI(
    title="SDN T+15 Traffic Predictor",
    description="ONOS cihaz verilerinden 15 saniye sonrası paket sayısını tahmin eder ve anomalileri tespit eder.",
    version="2.0"
)

# === CORS Ayarları ===
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# === Cihaz Listesi ===
@app.get("/devices")
def get_devices():
    device_url = f"http://{ONOS_IP}:{ONOS_PORT}/onos/v1/devices"
    device_resp = requests.get(device_url, auth=AUTH)
    if device_resp.status_code != 200:
        return {"error": f"ONOS devices API hatası: {device_resp.status_code}"}

    devices_raw = device_resp.json().get('devices', [])
    devices = {d['id']: {
        "id": d['id'],
        "flow_count": 0,
        "total_packets": 0,
        "total_bytes": 0,
        "avg_packet_size": 0,
        "link_count": 0
    } for d in devices_raw}

    flow_url = f"http://{ONOS_IP}:{ONOS_PORT}/onos/v1/flows"
    flow_resp = requests.get(flow_url, auth=AUTH)
    if flow_resp.status_code == 200:
        for f in flow_resp.json().get('flows', []):
            device_id = f.get('deviceId')
            if device_id in devices:
                devices[device_id]['flow_count'] += 1
                devices[device_id]['total_packets'] += f.get('packets', 0)
                devices[device_id]['total_bytes'] += f.get('bytes', 0)

    for d in devices.values():
        if d['flow_count'] > 0:
            d['avg_packet_size'] = d['total_bytes'] / d['flow_count']

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

# === Tahmin & Anomali Tespiti ===
@app.post("/predict/{device_id}")
def predict_future_packets(device_id: str):
    flow_url = f"http://{ONOS_IP}:{ONOS_PORT}/onos/v1/flows/{device_id}"
    link_url = f"http://{ONOS_IP}:{ONOS_PORT}/onos/v1/links"
    flow_resp = requests.get(flow_url, auth=AUTH)
    link_resp = requests.get(link_url, auth=AUTH)

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

    if model is None or scaler is None:
        return {"error": "Model veya scaler yüklenemedi."}

    # === Tahmin Girdisi ve Çıktısı ===
    input_array = np.array([[avg_packet_size, flow_count, total_packets, total_bytes, link_count]])
    scaled_input = scaler.transform(input_array)
    predicted_total_packets = model.predict(scaled_input)[0][0]

    # === Anomali Tespiti ===
    threshold = 1000  # İyi kalibre edilmiş eşik
    anomaly = abs(predicted_total_packets - total_packets) > threshold

    return {
        "device_id": device_id,
        "flow_count": flow_count,
        "total_packets": total_packets,
        "total_bytes": total_bytes,
        "avg_packet_size": avg_packet_size,
        "link_count": link_count,
        "predicted_total_packets_t_plus_15": int(predicted_total_packets),
        "anomaly": bool(anomaly)
    }

# === Topoloji ===
@app.get("/topology")
def get_topology():
    devices_resp = requests.get(f"http://{ONOS_IP}:{ONOS_PORT}/onos/v1/devices", auth=AUTH)
    hosts_resp = requests.get(f"http://{ONOS_IP}:{ONOS_PORT}/onos/v1/hosts", auth=AUTH)
    links_resp = requests.get(f"http://{ONOS_IP}:{ONOS_PORT}/onos/v1/links", auth=AUTH)

    devices = devices_resp.json().get("devices", []) if devices_resp.status_code == 200 else []
    hosts = hosts_resp.json().get("hosts", []) if hosts_resp.status_code == 200 else []
    links = links_resp.json().get("links", []) if links_resp.status_code == 200 else []

    return {"devices": devices, "hosts": hosts, "links": links}

