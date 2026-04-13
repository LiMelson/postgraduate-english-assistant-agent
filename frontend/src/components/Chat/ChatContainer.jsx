import React, { useState, useRef, useEffect, useContext } from 'react';
import Message from './Message';
import ChatInput from './ChatInput';
import { askQuestion } from '../../services/api';
import { ThemeContext } from '../../context/ThemeContext';

const ChatContainer = () => {
  const { isDark } = useContext(ThemeContext);
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isGenerating, setIsGenerating] = useState(false);
  const [hasSentMessage, setHasSentMessage] = useState(false);
  const [conversationId, setConversationId] = useState(() => {
    return 'conversation_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
  });
  const messagesEndRef = useRef(null);
  const abortControllerRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async (question) => {
    setHasSentMessage(true);
    // 添加用户消息
    setMessages((prev) => [...prev, { role: 'user', content: question }]);
    setIsLoading(true);
    setIsGenerating(true);

    // 创建AbortController实例
    const abortController = new AbortController();
    abortControllerRef.current = abortController;

    try {
      // 保存当前消息数量，用于识别新的assistant消息位置
      const messageCount = messages.length;
      
      await askQuestion(question, (data, type) => {
        // 当开始收到流式数据时，设置isLoading为false，隐藏加载中状态
        setIsLoading(false);
        
        // 使用函数式更新确保获取最新的状态
        setMessages((prevMessages) => {
          // 查找是否已经有对应这条用户消息的assistant消息
          // 应该是在用户消息之后的第一条assistant消息
          const userMessageIndex = prevMessages.findLastIndex(msg => msg.role === 'user' && msg.content === question);
          
          if (userMessageIndex !== -1) {
            // 检查用户消息之后是否已经有assistant消息
            const assistantMessageIndex = prevMessages.findIndex(
              (msg, index) => index > userMessageIndex && msg.role === 'assistant'
            );
            
            if (assistantMessageIndex !== -1) {
              // 更新现有的assistant消息
              const updatedMessages = [...prevMessages];
              updatedMessages[assistantMessageIndex] = {
                ...updatedMessages[assistantMessageIndex],
                content: data.explanation || '抱歉，没有找到相关信息。',
                type: type
              };
              return updatedMessages;
            } else {
              // 添加新的assistant消息
              return [...prevMessages, { role: 'assistant', content: data.explanation || '抱歉，没有找到相关信息。', type: type }];
            }
          } else {
            // 如果找不到用户消息，添加新的assistant消息
            return [...prevMessages, { role: 'assistant', content: data.explanation || '抱歉，没有找到相关信息。', type: type }];
          }
        });
      }, abortController.signal, conversationId);
    } catch (error) {
      // 忽略中止错误
      if (error.name !== 'AbortError') {
        // 使用函数式更新确保获取最新的状态
        setMessages((prevMessages) => {
          // 查找最新的用户消息
          const userMessageIndex = prevMessages.findLastIndex(msg => msg.role === 'user');
          
          if (userMessageIndex !== -1) {
            // 检查用户消息之后是否已经有assistant消息
            const assistantMessageIndex = prevMessages.findIndex(
              (msg, index) => index > userMessageIndex && msg.role === 'assistant'
            );
            
            if (assistantMessageIndex !== -1) {
              // 更新现有的assistant消息
              const updatedMessages = [...prevMessages];
              updatedMessages[assistantMessageIndex] = {
                ...updatedMessages[assistantMessageIndex],
                content: '抱歉，发生了错误，请稍后重试。'
              };
              return updatedMessages;
            } else {
              // 添加新的assistant消息
              return [...prevMessages, { role: 'assistant', content: '抱歉，发生了错误，请稍后重试。' }];
            }
          } else {
            // 如果找不到用户消息，添加新的assistant消息
            return [...prevMessages, { role: 'assistant', content: '抱歉，发生了错误，请稍后重试。' }];
          }
        });
      }
    } finally {
      setIsLoading(false);
      setIsGenerating(false);
      abortControllerRef.current = null;
    }
  };

  const handleStop = () => {
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
      setIsGenerating(false);
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-[calc(100vh-64px)]">
      <div className="flex-1 overflow-y-auto p-4 sm:p-6 chat-container">
        {messages.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-full text-center px-4">
            <div className="text-6xl mb-6">📝</div>
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-3">
              欢迎使用考研英语辅助Agent
            </h2>
            <p className="text-gray-600 dark:text-gray-400 max-w-md leading-relaxed mb-8">
              输入你的问题，我会帮你查找真题、解析知识点并生成思维导图
            </p>
            {!hasSentMessage && (
              <div className="w-full max-w-2xl">
                <ChatInput onSend={handleSend} onStop={handleStop} disabled={isLoading} isGenerating={isGenerating} />
              </div>
            )}
          </div>
        ) : (
          <div className="max-w-4xl mx-auto">
            {messages.map((msg, index) => (
              <Message key={index} role={msg.role} content={msg.content} type={msg.type} />
            ))}
            {isLoading && (
              <div className="flex mb-4">
                <div className="mr-3 w-10 h-10 rounded-full flex items-center justify-center" style={{ backgroundColor: isDark ? '#1e1e1e' : '#f3f4f6' }}>
                  <span className="text-xl">🤖</span>
                </div>
                <div className="message-bubble px-6 py-4 rounded-xl rounded-tl-md shadow-sm" style={{ backgroundColor: isDark ? '#1e1e1e' : '#f3f4f6' }}>
                  <div className="flex space-x-2">
                    <div className="w-2 h-2 rounded-full loading-dot" style={{ backgroundColor: isDark ? '#6b7280' : '#9ca3af', animationDelay: '0ms' }}></div>
                    <div className="w-2 h-2 rounded-full loading-dot" style={{ backgroundColor: isDark ? '#6b7280' : '#9ca3af', animationDelay: '150ms' }}></div>
                    <div className="w-2 h-2 rounded-full loading-dot" style={{ backgroundColor: isDark ? '#6b7280' : '#9ca3af', animationDelay: '300ms' }}></div>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
        )}
      </div>
      {hasSentMessage && (
        <div className="p-4 sm:p-6">
          <div className="max-w-4xl mx-auto">
            <ChatInput onSend={handleSend} onStop={handleStop} disabled={isLoading} isGenerating={isGenerating} />
          </div>
        </div>
      )}
    </div>
  );
};

export default ChatContainer;
