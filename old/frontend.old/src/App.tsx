import { useEffect, useState } from "react";
import * as types from "./types/NetworkDevice";
console.log("Types import:", types);

import DeviceTable from "./components/DeviceTable";
import TopologyGraph from "./components/TopologyGraph";

interface DeviceData {
  id?: string;
  device_id?: string;
  flow_count: number;
  total_packets: number;
  total_bytes: number;
  avg_packet_size: number;
  link_count: number;
  predicted_total_packets_t_plus_15?: number;
  anomaly: boolean;
}

function App() {
  const [devices, setDevices] = useState<DeviceData[]>([]);
  const [lastUpdate, setLastUpdate] = useState<string>("");

  const fetchDevicesAndPredict = async () => {
    try {
      const res = await fetch("http://127.0.0.1:8000/devices");
      const deviceData: DeviceData[] = await res.json();

      const devicesWithPredictions = await Promise.all(
        deviceData.map(async (device) => {
          try {
            const predictRes = await fetch(`http://127.0.0.1:8000/predict/${device.id}`, {
              method: "POST",
            });
            const predictData = await predictRes.json();
            return {
              ...device,
              predicted_total_packets_t_plus_15: predictData.predicted_total_packets_t_plus_15,
              anomaly: predictData.anomaly
            };
          } catch (error) {
            console.error(`Tahmin hatası (${device.id}):`, error);
            return device;
          }
        })
      );

      setDevices(devicesWithPredictions);
      setLastUpdate(new Date().toLocaleTimeString());
    } catch (err) {
      console.error("API hatası:", err);
    }
  };

  useEffect(() => {
    fetchDevicesAndPredict(); // İlk çalıştır
    const interval = setInterval(fetchDevicesAndPredict, 5000); // 5 saniyede bir güncelle
    return () => clearInterval(interval); // Bileşen unmount olursa temizle
  }, []);

  return (
    <div style={{ 
      padding: "20px",
      maxWidth: "1200px",
      margin: "0 auto",
      width: "100%",
      display: "flex",
      flexDirection: "column",
      alignItems: "center"
    }}>
      <h1>SDN Anomaly Detection Panel</h1>

      <h2>Ağ Topolojisi</h2>
      <div style={{ width: "100%" }}>
        <TopologyGraph devices={devices} />
      </div>

      <h2>
        Cihazlar ve Tahminler
        {lastUpdate && <span style={{ fontSize: "0.8em", marginLeft: "10px", color: "#666" }}>
          (Son güncelleme: {lastUpdate})
        </span>}
      </h2>
      <div style={{ 
        width: "100%",
        display: "flex",
        justifyContent: "center"
      }}>
        <div style={{ 
          width: "90%",
          maxWidth: "1000px"
        }}>
          <DeviceTable devices={devices} />
        </div>
      </div>
    </div>
  );
}

export default App;
