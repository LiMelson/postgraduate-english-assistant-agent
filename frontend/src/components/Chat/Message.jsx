import React, { useContext } from 'react';
import { ThemeContext } from '../../context/ThemeContext';
import MarkdownIt from 'markdown-it';

const md = new MarkdownIt({
  html: true,
  linkify: true,
  typographer: true
});

const Message = ({ role, content, type }) => {
  const isUser = role === 'user';
  const { isDark } = useContext(ThemeContext);
  
  // 渲染Markdown内容
  const renderMarkdown = (text) => {
    const html = md.render(text);
    return { __html: html };
  };
  
  // 根据type字段显示不同的图标
  const getTypeIcon = () => {
    if (type === 'search') {
      return '🔍';
    } else if (type === 'direct') {
      return '💬';
    } else {
      return '';
    }
  };
  
  return (
    <div className={`mb-4 ${isUser ? 'flex justify-end' : 'flex'}`}>
      {!isUser && (
        <div className="mr-3 w-10 h-10 rounded-full flex items-center justify-center" style={{ backgroundColor: isDark ? '#1e1e1e' : '#f3f4f6' }}>
          <span className="text-xl">🤖</span>
        </div>
      )}
      <div className={`message-bubble max-w-3xl px-6 py-4 rounded-xl shadow-sm ${isUser ? 'rounded-tr-md' : 'rounded-tl-md'}`} style={{
        backgroundColor: isUser ? (isDark ? '#333333' : '#3b82f6') : (isDark ? '#1e1e1e' : '#f3f4f6'),
        color: isUser ? 'white' : (isDark ? '#e0e0e0' : '#1f2937')
      }}>
        <div className="flex justify-between items-start">
          <div 
            className="text-sm sm:text-base flex-1"
            dangerouslySetInnerHTML={renderMarkdown(content)}
          />
          {!isUser && type && (
            <div className="ml-2 text-xs opacity-70">
              {getTypeIcon()}
            </div>
          )}
        </div>
      </div>
      {isUser && (
        <div className="ml-3 w-10 h-10 rounded-full flex items-center justify-center" style={{ backgroundColor: isDark ? '#1e1e1e' : '#f3f4f6' }}>
          <span className="text-xl">👤</span>
        </div>
      )}
    </div>
  );
};

export default Message;