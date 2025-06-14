import { useEffect, useState } from "react";
import * as types from "./types/NetworkDevice";
console.log("Types import:", types);

import DeviceTable from "./components/DeviceTable";
import TopologyGraph from "./components/TopologyGraph";

function App() {
  const [devices, setDevices] = useState<(NetworkDevice & { anomaly?: number })[]>([]);
  const [lastUpdate, setLastUpdate] = useState<string>("");

  const fetchDevicesAndPredict = async () => {
    try {
      const res = await fetch("http://127.0.0.1:8000/devices");
      const deviceData: NetworkDevice[] = await res.json();

      const devicesWithAnomaly = await Promise.all(
        deviceData.map(async (device) => {
          const predictRes = await fetch(`http://127.0.0.1:8000/predict/${device.id}`, {
            method: "POST",
          });
          const predictData = await predictRes.json();
          return { ...device, anomaly: predictData.anomaly };
        })
      );

      setDevices(devicesWithAnomaly);
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
      <h1>t+15 Anomaly Prediction</h1>

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
