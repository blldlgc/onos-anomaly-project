import pandas as pd

# CSV'leri oku
df_devices = pd.read_csv('onos_devices.csv')
df_flows = pd.read_csv('onos_flows.csv')
df_links = pd.read_csv('onos_links.csv')

# Cihaz başına flow özelliklerini topla
flow_stats = df_flows.groupby('deviceId').agg(
    flow_count=('flowId', 'count'),
    total_packets=('packets', 'sum'),
    total_bytes=('bytes', 'sum'),
    avg_packet_size=('bytes', lambda x: (x / (df_flows['packets'] + 1)).mean())  # basit avg hesaplama
).reset_index()

# Cihaz başına link sayısı
link_counts = df_links.groupby('src').size().reset_index(name='link_count')

# Cihaz bilgileriyle birleştir
df_final = df_devices.merge(flow_stats, left_on='id', right_on='deviceId', how='left')
df_final = df_final.merge(link_counts, left_on='id', right_on='src', how='left')

# Eksik değerleri 0 ile doldur
df_final.fillna(0, inplace=True)

# Label ekle (manuel kurala göre)
df_final['anomaly'] = df_final.apply(
    lambda row: 1 if (row['flow_count'] > 5 and row['avg_packet_size'] > 1000) else 0,
    axis=1
)

# Gereksiz kolonları sil
df_final.drop(columns=['src', 'deviceId'], inplace=True)

# Son hali CSV'ye kaydet
df_final.to_csv('sdn_features.csv', index=False)
print("Özellik dosyası 'sdn_features.csv' oluşturuldu.")
