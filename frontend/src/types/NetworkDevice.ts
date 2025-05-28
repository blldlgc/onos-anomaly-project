export interface NetworkDevice {
  id: string;
  flow_count: number;
  total_packets: number;
  total_bytes: number;
  avg_packet_size: number;
  link_count: number;
}
