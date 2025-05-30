import React, { useEffect, useState, useRef } from "react";
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

interface TopologyGraphProps {
  devices: NetworkDevice[];
}

const TopologyGraph: React.FC<TopologyGraphProps> = ({ devices }) => {
  const [elements, setElements] = useState<any[]>([]);
  const [layout, setLayout] = useState<any>({
    name: "cose",
    idealEdgeLength: 200,
    nodeOverlap: 50,
    refresh: 20,
    fit: true,
    padding: 100,
    randomize: false,
    componentSpacing: 300,
    nodeRepulsion: 15000,
    edgeElasticity: 200,
    nestingFactor: 1.5,
    gravity: 0.5,
    numIter: 2000,
    initialTemp: 300,
    coolingFactor: 0.98,
    animate: true,
    animateFilter: () => true
  });
  const cyRef = useRef<any>(null);

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

        setElements([...nodes, ...edges]);
      } catch (err) {
        console.error("Topology API hatası:", err);
      }
    };

    fetchTopology();
  }, []);

  useEffect(() => {
    if (cyRef.current) {
      const cy = cyRef.current;
      const layout = cy.layout({
        name: "cose",
        idealEdgeLength: 200,
        nodeOverlap: 50,
        refresh: 20,
        fit: true,
        padding: 100,
        randomize: false,
        componentSpacing: 300,
        nodeRepulsion: 15000,
        edgeElasticity: 200,
        nestingFactor: 1.5,
        gravity: 0.5,
        numIter: 2000,
        initialTemp: 300,
        coolingFactor: 0.98,
        animate: true,
        animateFilter: () => true
      });
      layout.run();
    }
  }, [elements]);

  return (
    <div style={{ height: "800px" }}>
      <CytoscapeComponent
        elements={elements}
        style={{ width: "100%", height: "100%" }}
        layout={layout}
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
        cy={(cy) => {
          cyRef.current = cy;
        }}
      />
    </div>
  );
};

export default TopologyGraph;
