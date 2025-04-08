import React, { useState } from 'react';
import axios from 'axios';
import './login.css'; // We'll reuse the login styles
import { Link } from 'react-router-dom';

export const Register = () => {
  const [username, setUsername] = useState('');
  const [registrationKey, setRegistrationKey] = useState('');
  const [error, setError] = useState('');
  const [isRegistered, setIsRegistered] = useState(false);

  const handleRegister = async (e) => {
    e.preventDefault();
    setError('');
    
    try {
      const response = await axios.post(
        'http://localhost:10001/register/uname',
        { uname: username }
      );

      setRegistrationKey(response.data.token);
      setIsRegistered(true);
    } catch (error) {
      console.error('Registration failed:', error);
      setError('Registration failed. Please try again.');
    }
  };

  return (
    <div className="login-container">
      <h2>Register Account</h2>
      {!isRegistered ? (
        <form className="login-form" onSubmit={handleRegister}>
          <input
            type="text"
            placeholder="Choose a Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
          <button type="submit">Register</button>
          {error && <div className="error-message">{error}</div>}
        </form>
      ) : (
        <div className="login-form">
          <div style={{ marginBottom: '20px', textAlign: 'center' }}>
            Registration successful! Please save your authentication key:
          </div>
          <div style={{ 
            padding: '15px', 
            backgroundColor: 'var(--bg-primary)', 
            borderRadius: '8px',
            wordBreak: 'break-all',
            marginBottom: '20px'
          }}>
            {registrationKey}
          </div>
          <div style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', textAlign: 'center' }}>
            Keep this key safe - you'll need it to log in!
          </div>
        </div>
      )}
      <div className="create-account">
        <Link to="/login">Already have an account? Log in →</Link>
      </div>
    </div>
  );
};

export default Register; 
