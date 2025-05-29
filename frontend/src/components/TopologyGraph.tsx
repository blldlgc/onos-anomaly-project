import React, { useEffect, useState } from "react";
import CytoscapeComponent from "react-cytoscapejs";

interface NetworkDevice {
  id: string;
  annotations?: {
    datapathDescription?: string;
  };
  anomaly?: number;
}

interface NetworkLink {
  src: {
    device: string;
    port: string;
  };
  dst: {
    device: string;
    port: string;
  };
}

interface TopologyData {
  devices: NetworkDevice[];
  links: NetworkLink[];
}

const TopologyGraph: React.FC = () => {
  const [elements, setElements] = useState<any[]>([]);

  useEffect(() => {
    const fetchTopology = async () => {
      try {
        const res = await fetch("http://127.0.0.1:8000/topology");
        const data: TopologyData = await res.json();

        const filteredDevices = data.devices.filter(
          (d) => !d.id.endsWith("/None")
        );

        const nodes = filteredDevices.map((device) => ({
          data: {
            id: device.id,
            label: device.annotations?.datapathDescription || device.id,
          },
        }));

        const edges = data.links.map((link, index) => ({
          data: {
            id: `link-${index}`,
            source: link.src.device,
            target: link.dst.device,
            label: `${link.src.port} ➔ ${link.dst.port}`,
          },
        }));

        console.log("Edges:", edges);

        setElements([...nodes, ...edges]);
      } catch (err) {
        console.error("Topology API hatası:", err);
      }
    };

    fetchTopology();
  }, []);

  return (
    <div style={{ height: "800px" }}>
      <CytoscapeComponent
        elements={elements}
        style={{ width: "100%", height: "100%" }}
        layout={{
          name: "cose",
          idealEdgeLength: 150,
          nodeOverlap: 20,
          refresh: 20,
          fit: true,
          padding: 50,
          randomize: true,
          componentSpacing: 200,
          nodeRepulsion: 8000,
          edgeElasticity: 100,
          nestingFactor: 1.2,
          gravity: 1,
          numIter: 1000,
          initialTemp: 200,
          coolingFactor: 0.95,
          animate: true,
        }}
        stylesheet={[
          {
            selector: "node",
            style: {
              label: "data(label)",
              "text-valign": "center",
              "text-halign": "center",
              "background-color": "#007acc",
              color: "#000",
              "text-outline-width": 0,
              width: 50,
              height: 50,
            },
          },
          {
            selector: "edge",
            style: {
              label: "data(label)",
              "line-color": "#aaa",
              "target-arrow-color": "#aaa",
              "target-arrow-shape": "triangle",
              "curve-style": "bezier",
              width: 2,
              color: "#000",
              "font-size": "8px",
            },
          },
        ]}
      />
    </div>
  );
};

export default TopologyGraph;
