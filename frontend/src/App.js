// frontend/src/App.js

import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  // State to store the message from the backend
  const [message, setMessage] = useState('Loading...');

  useEffect(() => {
    // Function to fetch data from the backend
    const fetchData = async () => {
      try {
        const response = await fetch('http://127.0.0.1:8000/');
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const data = await response.json();
        setMessage(data.message); // Assuming the backend returns { "message": "..." }
      } catch (error) {
        setMessage(`Failed to connect to backend: ${error.message}`);
      }
    };

    fetchData();
  }, []); // The empty array ensures this effect runs only once when the component mounts

  return (
    <div className="App">
      <header className="App-header">
        <h1>WellNest Platform</h1>
        <p>Status: {message}</p>
      </header>
    </div>
  );
}

export default App;