export interface NetworkDevice {
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
