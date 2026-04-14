import React, { useContext } from 'react';
import { ThemeContext } from '../../context/ThemeContext';

const Button = ({ 
  children, 
  variant = 'primary', 
  size = 'medium', 
  className = '', 
  ...props 
}) => {
  const { isDark } = useContext(ThemeContext);
  const baseClasses = 'inline-flex items-center justify-center font-medium rounded-lg transition-all focus:outline-none focus:ring-2 focus:ring-offset-2 shadow-sm hover:shadow-md';
  
  const sizes = {
    small: 'px-3 py-1.5 text-sm',
    medium: 'px-4 py-2 text-sm sm:text-base',
    large: 'px-6 py-3 text-base',
  };

  const getButtonStyles = () => {
    if (variant === 'primary') {
      return {
        backgroundColor: isDark ? '#333333' : '#3b82f6',
        color: 'white',
        ':hover': { backgroundColor: isDark ? '#444444' : '#2563eb' },
        ':focus': { ringColor: isDark ? '#6b7280' : '#93c5fd' }
      };
    } else if (variant === 'secondary') {
      return {
        backgroundColor: isDark ? '#333333' : '#f3f4f6',
        color: isDark ? '#e0e0e0' : '#1f2937',
        ':hover': { backgroundColor: isDark ? '#444444' : '#e5e7eb' },
        ':focus': { ringColor: isDark ? '#6b7280' : '#9ca3af' }
      };
    } else if (variant === 'ghost') {
      return {
        backgroundColor: 'transparent',
        color: isDark ? '#e0e0e0' : '#1f2937',
        ':hover': { backgroundColor: isDark ? '#1e1e1e' : '#f9fafb' },
        ':focus': { ringColor: isDark ? '#6b7280' : '#9ca3af' }
      };
    }
    return {};
  };

  return (
    <button
      className={`${baseClasses} ${sizes[size]} ${className}`}
      style={getButtonStyles()}
      {...props}
    >
      {children}
    </button>
  );
};

export default Button;
