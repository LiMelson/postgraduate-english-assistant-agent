import React, { useContext } from 'react';
import { ThemeProvider, ThemeContext } from './context/ThemeContext';
import Header from './components/Layout/Header';
import ChatContainer from './components/Chat/ChatContainer';

function AppContent() {
  const { isDark } = useContext(ThemeContext);
  
  return (
    <div className="min-h-screen transition-colors duration-300" style={{ backgroundColor: isDark ? '#171718ff' : '#f9fafb' }}>
      <Header />
      <main>
        <ChatContainer />
      </main>
    </div>
  );
}

function App() {
  return (
    <ThemeProvider>
      <AppContent />
    </ThemeProvider>
  );
}

export default App;
