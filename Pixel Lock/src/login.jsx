import React, { useState } from 'react';
import axios from 'axios';
import './login.css';
import { Link } from 'react-router-dom';

export const LogIn = ({ handleLogin }) => {
  const [username, setUsername] = useState('');
  const [authToken, setAuthToken] = useState('');
  const [rememberMe, setRememberMe] = useState(false);
  const [error, setError] = useState('');

  const handleLoginClick = async (e) => {
    e.preventDefault(); // Prevent form submission
    setError(''); // Clear previous errors
    
    try {
      const response = await axios.post(
        'http://localhost:10001/login',
        { uname: username, auth_token: authToken },
        { withCredentials: true }
      );

      const thumbnails = response.data.thumbnail.map((base64String, index) => ({
        id: index,
        src: `data:image/jpg;base64,${base64String}`,
        alt: `Image ${index}`
      }));

      handleLogin(thumbnails);
    } catch (error) {
      console.error('Login failed:', error);
      setError('Invalid credentials. Please try again.');
    }
  };

  return (
    <div className="login-container">
      <h2>Member Login</h2>
      <form className="login-form" onSubmit={handleLoginClick}>
        <input
          type="text"
          placeholder="Email or Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <input
          type="password"
          placeholder="Password"
          value={authToken}
          onChange={(e) => setAuthToken(e.target.value)}
        />
        
        {/* <div className="form-helpers">
          <label>
            <input
              type="checkbox"
              checked={rememberMe}
              onChange={(e) => setRememberMe(e.target.checked)}
            /> Remember me
          </label>
          <a href="#forgot-password">Forgot your password?</a>
        </div> */}

        <button type="submit">Log In</button>
        
        {error && <div className="error-message">{error}</div>}
      </form>

      <div className="create-account">
        <Link to="/register">Create your account →</Link>
      </div>
    </div>
  );
};

export default LogIn;

