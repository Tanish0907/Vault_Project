import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';
import './styles.css';
import './theme.css';
import Gallery from './Gallery';
import LogIn from './login';
import Register from './register';

function App() {
  const [imageList, setImageList] = useState([]);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  const handleLogin = (data) => {
    setImageList(data);
    setIsAuthenticated(true);
  };

  return (
    <Router>
      <Routes>
        <Route
          path="/login"
          element={isAuthenticated ? <Navigate to="/gallery" /> : <LogIn handleLogin={handleLogin} />}
        />
        <Route
          path="/register"
          element={isAuthenticated ? <Navigate to="/gallery" /> : <Register />}
        />
        <Route
          path="/gallery"
          element={isAuthenticated ? <Gallery imageList={imageList} /> : <Navigate to="/login" />}
        />
        <Route path="*" element={<Navigate to={isAuthenticated ? "/gallery" : "/login"} />} />
      </Routes>
    </Router>
  );
}

export default App;

