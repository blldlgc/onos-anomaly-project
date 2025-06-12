import * as types from "../types/NetworkDevice";
console.log("Types import:", types);

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

interface DeviceTableProps {
  devices: DeviceData[];
}

const DeviceTable: React.FC<DeviceTableProps> = ({ devices }) => {
  console.log('API\'dan gelen ham veri:', JSON.stringify(devices, null, 2));

  const formatNumber = (num: number) => {
    if (isNaN(num) || !isFinite(num)) {
      return '-';
    }
    return new Intl.NumberFormat('tr-TR').format(num);
  };

  const formatBytes = (bytes: number) => {
    if (isNaN(bytes) || !isFinite(bytes)) {
      return '-';
    }
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
    if (bytes === 0) return '0 Byte';
    const i = Math.floor(Math.log(bytes) / Math.log(1024));
    return `${(bytes / Math.pow(1024, i)).toFixed(2)} ${sizes[i]}`;
  };

  return (
    <div style={{ overflowX: 'auto' }}>
      <table style={{ 
        borderCollapse: 'collapse', 
        width: '100%', 
        marginTop: '20px',
        boxShadow: '0 0 20px rgba(0, 0, 0, 0.1)'
      }}>
        <thead>
          <tr style={{ backgroundColor: '#f8f9fa' }}>
            <th style={{ padding: '12px', textAlign: 'left', borderBottom: '2px solid #dee2e6' }}>Cihaz ID</th>
            <th style={{ padding: '12px', textAlign: 'left', borderBottom: '2px solid #dee2e6' }}>Flow Sayısı</th>
            <th style={{ padding: '12px', textAlign: 'left', borderBottom: '2px solid #dee2e6' }}>Toplam Paket</th>
            <th style={{ padding: '12px', textAlign: 'left', borderBottom: '2px solid #dee2e6' }}>Toplam Veri</th>
            <th style={{ padding: '12px', textAlign: 'left', borderBottom: '2px solid #dee2e6' }}>Ort. Paket Boyutu</th>
            <th style={{ padding: '12px', textAlign: 'left', borderBottom: '2px solid #dee2e6' }}>Bağlantı Sayısı</th>
            <th style={{ padding: '12px', textAlign: 'left', borderBottom: '2px solid #dee2e6' }}>Tahmini Paket (t+15)</th>
            <th style={{ padding: '12px', textAlign: 'left', borderBottom: '2px solid #dee2e6' }}>Anomali</th>
          </tr>
        </thead>
        <tbody>
          {devices.map((device) => (
            <tr key={device.id || device.device_id} style={{ 
              backgroundColor: device.anomaly ? '#fff3f3' : '#ffffff',
              transition: 'background-color 0.3s ease'
            }}>
              <td style={{ padding: '12px', borderBottom: '1px solid #dee2e6' }}>{device.id || device.device_id}</td>
              <td style={{ padding: '12px', borderBottom: '1px solid #dee2e6' }}>{formatNumber(device.flow_count)}</td>
              <td style={{ padding: '12px', borderBottom: '1px solid #dee2e6' }}>{formatNumber(device.total_packets)}</td>
              <td style={{ padding: '12px', borderBottom: '1px solid #dee2e6' }}>{formatBytes(device.total_bytes)}</td>
              <td style={{ padding: '12px', borderBottom: '1px solid #dee2e6' }}>{formatBytes(device.avg_packet_size)}</td>
              <td style={{ padding: '12px', borderBottom: '1px solid #dee2e6' }}>{formatNumber(device.link_count)}</td>
              <td style={{ padding: '12px', borderBottom: '1px solid #dee2e6' }}>{formatNumber(device.predicted_total_packets_t_plus_15 || 0)}</td>
              <td style={{ 
                padding: '12px', 
                borderBottom: '1px solid #dee2e6',
                color: device.anomaly ? '#dc3545' : '#28a745',
                fontWeight: 'bold'
              }}>
                {device.anomaly ? 'Evet' : 'Hayır'}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default DeviceTable;

