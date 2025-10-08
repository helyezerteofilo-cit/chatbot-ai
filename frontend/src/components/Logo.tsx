import React from 'react';
import logoImage from '../assets/logo.png';
import '../styles/Logo.css';

interface LogoProps {
  size?: 'small' | 'medium' | 'large';
}

const Logo: React.FC<LogoProps> = ({ size = 'medium' }) => {
  return (
    <div className={`logo logo-${size}`}>
      <img src={logoImage} alt="AI Chatbot Logo" className="logo-image" />
    </div>
  );
};

export default Logo;