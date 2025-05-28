import requests
import heapq

# ONOS API Ayarları
onos_url = "http://localhost:8181/onos/v1"
auth = ("onos", "rocks")

# ONOS'tan cihaz ve bağlantı verilerini al
devices = requests.get(f"{onos_url}/devices", auth=auth).json()["devices"]
links = requests.get(f"{onos_url}/links", auth=auth).json()["links"]

# Graph oluştur
graph = {}
for device in devices:
    graph[device["id"]] = []

for link in links:
    src = link["src"]["device"]
    dst = link["dst"]["device"]
    graph[src].append(dst)
    graph[dst].append(src)  # çift yönlü bağlantı

# Dijkstra algoritması
def dijkstra(graph, start, end):
    queue = [(0, start, [])]
    visited = set()
    while queue:
        (cost, node, path) = heapq.heappop(queue)
        if node in visited:
            continue
        path = path + [node]
        if node == end:
            return (cost, path)
        visited.add(node)
        for neighbor in graph.get(node, []):
            heapq.heappush(queue, (cost + 1, neighbor, path))
    return (float("inf"), [])

# Test: Bir cihazdan diğerine yol bulalım
source = input("Başlangıç cihaz ID'sini gir (ör: of:0000000000000001): ")
destination = input("Hedef cihaz ID'sini gir (ör: of:0000000000000004): ")
cost, path = dijkstra(graph, source, destination)

print(f"En kısa yol: {path}")
print(f"Toplam maliyet (hop sayısı): {cost}")
