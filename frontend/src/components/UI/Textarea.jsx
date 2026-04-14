import React, { useContext } from 'react';
import { ThemeContext } from '../../context/ThemeContext';

const Textarea = ({ placeholder, value, onChange, className = '', ...props }) => {
  const { isDark } = useContext(ThemeContext);
  
  return (
    <textarea
      placeholder={placeholder}
      value={value}
      onChange={onChange}
      className={`w-full p-3 rounded-lg focus:ring-2 focus:border-transparent resize-none shadow-sm transition-all ${className}`}
      style={{
        backgroundColor: isDark ? '#1e1e1e' : '#f9fafb',
        borderColor: isDark ? '#333333' : '#9ca3af',
        borderWidth: isDark ? '1px' : '2px',
        borderStyle: 'solid',
        color: isDark ? '#e0e0e0' : '#1f2937',
        placeholderColor: isDark ? '#6b7280' : '#9ca3af',
        ':hover': { borderColor: isDark ? '#444444' : '#6b7280' },
        ':focus': { ringColor: isDark ? '#6b7280' : '#9ca3af' }
      }}
      {...props}
    />
  );
};

export default Textarea;
