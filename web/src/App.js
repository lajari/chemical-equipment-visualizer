import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Bar } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

function App() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [history, setHistory] = useState([]);

  const fetchHistory = async () => {
    try {
      const res = await axios.get('http://127.0.0.1:8000/api/history/');
      setHistory(res.data);
    } catch (err) {
      console.error("Failed to fetch history");
    }
  };

  useEffect(() => {
    fetchHistory();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) {
      alert("Please choose a CSV file");
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
      const res = await axios.post('http://127.0.0.1:8000/api/upload/', formData);
      setResult(res.data);
      setError(null);
      fetchHistory();   // Refresh history after upload
    } catch (err) {
      console.error(err);
      setError("Upload failed. Check backend/CORS.");
    }
  };

  const handleClear = () => {
    setFile(null);
    setResult(null);
    setError(null);
    document.getElementById("fileInput").value = "";
  };

  const chartData = result ? {
    labels: Object.keys(result.type_distribution),
    datasets: [
      {
        label: 'Equipment Count',
        data: Object.values(result.type_distribution),
        backgroundColor: 'rgba(54, 162, 235, 0.6)',
      },
    ],
  } : null;

  return (
    <div style={{ 
      minHeight: '100vh', 
      background: '#f5f7fb', 
      padding: 20, 
      fontFamily: 'Arial' 
    }}>
      <div style={{ 
        maxWidth: 900, 
        margin: '0 auto', 
        background: '#fff', 
        padding: 20, 
        borderRadius: 8, 
        boxShadow: '0 0 10px rgba(0,0,0,0.1)' 
      }}>
        <h2 style={{ textAlign: 'center' }}>FOSSEE CSV Analyzer</h2>

        <form onSubmit={handleSubmit} style={{ textAlign: 'center' }}>
          <input
            id="fileInput"
            type="file"
            accept=".csv"
            onChange={(e) => setFile(e.target.files[0])}
          />
          <br /><br />
          <button type="submit" style={{ marginRight: 10 }}>Upload CSV</button>
          <button type="button" onClick={handleClear}>Clear</button>
        </form>

        {error && <p style={{ color: 'red', textAlign: 'center' }}>{error}</p>}

        {result && (
          <div style={{ marginTop: 20 }}>
            <h3>Summary (Table View)</h3>
            <table border="1" cellPadding="8" style={{ width: '100%', borderCollapse: 'collapse' }}>
              <tbody>
                <tr>
                  <td>Total Count</td>
                  <td>{result.total_count}</td>
                </tr>
                <tr>
                  <td>Average Flowrate</td>
                  <td>{result.avg_flowrate}</td>
                </tr>
                <tr>
                  <td>Average Pressure</td>
                  <td>{result.avg_pressure}</td>
                </tr>
                <tr>
                  <td>Average Temperature</td>
                  <td>{result.avg_temperature}</td>
                </tr>
              </tbody>
            </table>

            <h3 style={{ marginTop: 20 }}>Equipment Type Distribution</h3>
            <div style={{ maxWidth: 600, margin: '0 auto' }}>
              <Bar data={chartData} />
            </div>
          </div>
        )}

        <h3 style={{ marginTop: 30 }}>Upload History (Last 5)</h3>
        <table border="1" cellPadding="8" style={{ width: '100%', borderCollapse: 'collapse' }}>
          <thead>
            <tr>
              <th>Uploaded At</th>
              <th>Total Count</th>
              <th>Avg Flowrate</th>
              <th>Avg Pressure</th>
              <th>Avg Temperature</th>
            </tr>
          </thead>
          <tbody>
            {history.map((item, index) => (
              <tr key={index}>
                <td>{new Date(item.uploaded_at).toLocaleString()}</td>
                <td>{item.total_count}</td>
                <td>{item.avg_flowrate.toFixed(2)}</td>
                <td>{item.avg_pressure.toFixed(2)}</td>
                <td>{item.avg_temperature.toFixed(2)}</td>
              </tr>
            ))}
          </tbody>
        </table>

      </div>
    </div>
  );
}

export default App;
