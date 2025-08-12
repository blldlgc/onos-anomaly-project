# ONOS-Based Network Anomaly Detection and Digital Twin Project

This project is a prototype developed to detect network anomalies in a Software-Defined Networking (SDN) environment. The system aims to proactively identify potential attacks and anomalies by collecting live network data from an ONOS (Open Network Operating System) controller and applying machine learning algorithms on a digital twin model.

## 📜 Conference Paper

A scientific paper based on the findings and architecture of this project has been submitted to an international conference and is currently **under review**. Once the paper is accepted, the reference information and access link will be added here.

## ✨ Key Features

*   **Live Data Collection**: Gathers real-time data about hosts, links, and flows from the network using ONOS APIs.
*   **Feature Engineering**: Extracts meaningful features from raw network data for the machine learning models.
*   **ML-Powered Anomaly Detection**: Employs trained models to analyze network behavior and classify abnormal states (anomalies).
*   **Visual Interface**: A modern, React-based web UI to visualize the network topology, devices, and the results of anomaly predictions.
*   **Attack Simulation**: Capable of simulating various attack scenarios to generate training data.

## 🚀 Tech Stack

*   **Backend & Data Processing**:
    *   Python
    *   Flask / FastAPI (for the API server)
    *   Pandas (for data manipulation)
    *   Scikit-learn, TensorFlow/Keras (for machine learning models)
*   **Frontend**:
    *   React (with TypeScript)
    *   Vite (as the build tool)
    *   D3.js or a similar library (for topology visualization)
*   **SDN & Simulation**:
    *   ONOS (SDN Controller)
    *   Mininet (for network simulation)

## 🔧 Getting Started

Follow these steps to run the project on your local machine.

### Prerequisites

*   Python 3.8+
*   Node.js 16+
*   A running instance of ONOS and a Mininet environment.

### 1. Backend Setup

```bash
# Clone the repository
git clone <your-repo-url>
cd <project-directory>

# Install the required Python libraries
# Note: Ensure the requirements.txt file is in the correct path
pip install -r lab4/requirements.txt

# Start the ONOS API server
python onos_api_server.py
```

### 2. Frontend Setup

```bash
# Navigate to the frontend directory
cd frontend

# Install the required Node.js packages
npm install

# Start the development server
npm run dev
```

The application will be running by default at `http://localhost:5173`.

## 👥 Contributors

*   Bilal DALGIÇ
*   Betül ŞEN

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for more details.
