import { useState } from "react";

interface PredictFormProps {
  deviceId: string;
}

const PredictForm: React.FC<PredictFormProps> = ({ deviceId }) => {
  const [result, setResult] = useState<any>(null);

  const handlePredict = async () => {
    const response = await fetch(`http://127.0.0.1:8000/predict/${deviceId}`, {
      method: "POST",
    });
    const data = await response.json();
    setResult(data);
  };

  return (
    <div style={{ marginTop: "20px", padding: "10px", border: "1px solid gray" }}>
      <h3>Anomaly Tahmini</h3>
      <button onClick={handlePredict}>Tahmin Al</button>
      {result && (
        <pre>{JSON.stringify(result, null, 2)}</pre>
      )}
    </div>
  );
};

export default PredictForm;
