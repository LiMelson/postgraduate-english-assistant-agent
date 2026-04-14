import React from 'react';
import { useTheme } from '../../context/ThemeContext';

const Header = () => {
  const { isDark, toggleTheme } = useTheme();

  return (
    <header className="sticky top-0 z-50 bg-white border-b border-gray-200" style={{ backgroundColor: isDark ? '#1e1e1e' : 'white', borderColor: isDark ? '#333333' : '#e5e7eb' }}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center">
            <h1 className="text-xl font-bold" style={{ color: isDark ? '#e0e0e0' : '#1f2937' }}>
              📚 考研英语辅助Agent
            </h1>
          </div>
          <div className="flex items-center space-x-4">
            <button
              onClick={toggleTheme}
              aria-label="切换主题"
              className="inline-flex items-center justify-center px-4 py-2 rounded-lg transition-colors focus:outline-none focus:ring-2 focus:ring-gray-400"
              style={{ 
                backgroundColor: isDark ? '#333333' : '#f3f4f6',
                color: isDark ? '#e0e0e0' : '#1f2937',
                ':hover': { backgroundColor: isDark ? '#444444' : '#e5e7eb' }
              }}
            >
              {isDark ? '☀️ 明' : '🌙 暗'}
            </button>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
