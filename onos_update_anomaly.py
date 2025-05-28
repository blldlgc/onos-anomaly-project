import pandas as pd

df = pd.read_csv("sdn_features.csv")

# Yeni anomaly kuralı
df['anomaly'] = df.apply(
    lambda row: 1 if (row['flow_count'] > 20 or row['avg_packet_size'] < 50 or row['link_count'] > 5) else 0,
    axis=1
)

# Güncellenmiş CSV'yi kaydet
df.to_csv("sdn_features_updated.csv", index=False)
print("Anomaly güncellendi ve kaydedildi.")
