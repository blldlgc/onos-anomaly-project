import * as types from "../types/NetworkDevice";
console.log("Types import:", types);


interface DeviceTableProps {
  devices: (NetworkDevice & { anomaly?: number })[];
}

const DeviceTable: React.FC<DeviceTableProps> = ({ devices }) => {
  return (
    <table border={1} cellPadding={8}>
      <thead>
        <tr>
          <th>ID</th>
          <th>Flow Count</th>
          <th>Total Packets</th>
          <th>Total Bytes</th>
          <th>Avg Packet Size</th>
          <th>Link Count</th>
          <th>t+15 Anomaly Prediction</th>
        </tr>
      </thead>
      <tbody>
        {devices.map((device) => (
          <tr key={device.id}>
            <td>{device.id}</td>
            <td>{device.flow_count}</td>
            <td>{device.total_packets}</td>
            <td>{device.total_bytes}</td>
            <td>{device.avg_packet_size.toFixed(2)}</td>
            <td>{device.link_count}</td>
            <td style={{ color: device.anomaly === 1 ? "red" : "green", fontWeight: "bold" }}>
              {device.anomaly}
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default DeviceTable;

