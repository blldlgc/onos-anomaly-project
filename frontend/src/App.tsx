import { useEffect, useState } from "react";
import * as types from "./types/NetworkDevice";
console.log("Types import:", types);
import DeviceTable from "./components/DeviceTable";


function App() {
  const [devices, setDevices] = useState<(NetworkDevice & { anomaly?: number })[]>([]);

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
    <div style={{ padding: "20px" }}>
      <h1>SDN Anomaly Detection Panel</h1>
      <DeviceTable devices={devices} />
    </div>
  );
}

export default App;


