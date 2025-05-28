from flask import Flask, request, jsonify
import requests
import heapq

app = Flask(__name__)

# ONOS API ayarları
onos_url = "http://localhost:8181/onos/v1"
auth = ("onos", "rocks")

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

# API endpointi: /shortest_path?src=...&dst=...
@app.route('/shortest_path', methods=['GET'])
def get_shortest_path():
    src = request.args.get('src')
    dst = request.args.get('dst')

    # ONOS'tan cihaz ve bağlantı verilerini al
    devices = requests.get(f"{onos_url}/devices", auth=auth).json()["devices"]
    links = requests.get(f"{onos_url}/links", auth=auth).json()["links"]

    # Graph oluştur
    graph = {}
    for device in devices:
        graph[device["id"]] = []

    for link in links:
        src_dev = link["src"]["device"]
        dst_dev = link["dst"]["device"]
        graph[src_dev].append(dst_dev)
        graph[dst_dev].append(src_dev)

    # Dijkstra çalıştır
    cost, path = dijkstra(graph, src, dst)

    # JSON response
    return jsonify({
        "path": path,
        "cost": cost
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
